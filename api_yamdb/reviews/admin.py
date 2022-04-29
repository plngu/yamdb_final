from django.contrib import admin

from .models import ConfirmationCheck, User, Review, Comment

admin.site.register(ConfirmationCheck)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'first_name',
                    'last_name', 'bio', 'role')
    list_editable = ('role',)
    search_fields = ('username',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author', 'text', 'pub_date', 'score')
    search_fields = ('title', 'author')
    list_filter = ('pub_date', )
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'pub_date', 'review')
    search_fields = ('text', 'author')
    list_filter = ('pub_date', )
    empty_value_display = '-пусто-'
