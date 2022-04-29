from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import (Title, Review, Comment, User,
                            ConfirmationCheck, Genre, Category)


def validate_username(value):
    username = 'me'
    if username == value:
        raise serializers.ValidationError('Поле <username> '
                                          'не может иметь значение <me>')


class RegUserSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        max_length=150,
        validators=[validate_username,
                    UniqueValidator(queryset=User.objects.all())
                    ]
    )


class ConfirmationCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmationCheck
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        max_length=150,
        validators=[validate_username,
                    UniqueValidator(queryset=User.objects.all())
                    ]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date')

    def validate(self, data):
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if self.context['request'].method == 'PATCH':
            return data
        if Review.objects.filter(title=title_id, author=author).exists():
            raise serializers.ValidationError(
                'Отзыв на произведение уже оставлен')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'pub_date')
