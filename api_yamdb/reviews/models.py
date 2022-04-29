from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .validators import validate_year

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
USER_ROLES = (
    (USER, 'регулярный'),
    (MODERATOR, 'модератор'),
    (ADMIN, 'админ')
)


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=100,
        choices=USER_ROLES,
        default=USER,
        null=False,
        help_text='Роль пользователя',
    )

    @property
    def admin(self):
        if self.role == ADMIN:
            return True

    @property
    def moderator(self):
        if self.role == MODERATOR:
            return True

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class ConfirmationCheck(models.Model):
    username = models.CharField(
        'Пользователь',
        max_length=150,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=1000,
    )

    class Meta:
        verbose_name = 'Код подтверждения'
        verbose_name_plural = 'Коды подтверждения'

    def __str__(self):
        return self.confirmation_code


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг категории',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг жанра',
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тайтла',
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория тайтла',
    )
    genre = models.ManyToManyField(
        Genre,
        null=True,
        related_name='titles',
        verbose_name='Жанр тайтла',
    )
    year = models.IntegerField(
        null=True,
        validators=[validate_year],
        verbose_name='Год'
    )
    description = models.TextField(
        null=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Тайтл'
        verbose_name_plural = 'Тайтлы'


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(blank=False)
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    score = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1, 'Оценка не может быть ниже 1'),
                    MaxValueValidator(10, 'Оценка не может быть выше 10')),
        default=1,
        null=True,
    )

    class Meta:
        ordering = ('-pub_date', )
        constraints = (
            models.UniqueConstraint(fields=('author', 'title'),
                                    name='unique review'),
        )


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    text = models.TextField(blank=False)

    class Meta:
        ordering = ('-pub_date', )
