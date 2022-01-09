from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    username = models.CharField(
        'Логин', max_length=150, unique=True,)
    first_name = models.CharField(
        'Имя', max_length=150, blank=True,)
    last_name = models.CharField(
        'Фамилия', max_length=150, blank=True,)
    email = models.EmailField(
        'Почта',
        max_length=254,
        blank=False,
        unique=True,)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return f'{(self.username)}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Фолловер',
        related_name='follower')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='following')

    class Meta:
        verbose_name = 'Фолловер'
        verbose_name_plural = 'Фолловеры'
        ordering = ('-id',)
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_user'),)

    def __str__(self):
        return f'{(self.user)}'
