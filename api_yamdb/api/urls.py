from rest_framework import routers
from django.urls import include, path

from .views import (get_token, register_user, ReviewsViewSet,
                    CommentsViewSet, UserViewSet, TitleViewSet,
                    GenreViewSet, CategoryViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet,
                basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/'
                r'(?P<review_id>\d+)/comments',
                CommentsViewSet,
                basename='comments')


urlpatterns = [
    path('v1/auth/signup/', register_user, name='register_user'),
    path('v1/auth/token/', get_token, name='get_token'),
    path('v1/', include(router.urls))
]
