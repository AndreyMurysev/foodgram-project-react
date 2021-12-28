from django.contrib import admin
from django.conf import settings

from .models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'username',
                    'first_name',
                    'last_name',
                    'email',)
    list_filter = ('username', 'email',)
    empty_value_display = settings.VOID


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'user',
                    'author',)
    empty_value_display = settings.VOID
