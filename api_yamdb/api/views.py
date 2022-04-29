from django.conf import settings as s
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.response import Response
from rest_framework import status, filters, permissions, viewsets, mixins

from reviews.models import (ConfirmationCheck, User, Review,
                            Title, Genre, Category)
from .filters import TitleFilter
from .mixins import CreateUpdateDestroyMixin
from .permissions import Admin, IsAdminOrReadOnly
from .serializers import (ConfirmationCheckSerializer, RegUserSerializer,
                          UserSerializer, ReviewSerializer, CommentSerializer,
                          GenreSerializer, CategorySerializer,
                          TitleWriteSerializer, TitleReadSerializer)
from .token import get_token_or_code


class CustomViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = ConfirmationCheckSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    try:
        ConfirmationCheck.objects.get(
            confirmation_code=confirmation_code
        )
    except ConfirmationCheck.DoesNotExist:
        return Response({'Message': 'Incorrect confirmation_code!'},
                        status=status.HTTP_400_BAD_REQUEST
                        )
    token = get_token_or_code(user)
    return Response({'token': token}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = RegUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    user, result = User.objects.get_or_create(username=username, email=email)
    confirmation_code = get_token_or_code(user)
    ConfirmationCheck.objects.create(username=username,
                                     confirmation_code=confirmation_code)
    send_mail(subject='Confirmation code to get token',
              message=f'Код подтвердения: {confirmation_code}',
              from_email=s.EMAIL,
              recipient_list=[email])
    return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    permission_classes = [Admin]
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        user = self.get_queryset().get(username=request.user.username)
        if request.method == 'PATCH':
            serializer = self.get_serializer(user,
                                             data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenreViewSet(CustomViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CustomViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('-pk')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewsViewSet(CreateUpdateDestroyMixin):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(CreateUpdateDestroyMixin):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
