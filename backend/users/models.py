from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint
from rest_framework.exceptions import ValidationError

from foodgram.constants import EMAIL_LENGTH


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]
    email = models.EmailField(
        verbose_name="email address",
        max_length=EMAIL_LENGTH,
        unique=True,
    )

    class Meta:
        ordering = ("username", "email")
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        related_name="subscriber",
        verbose_name="Подписчик",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name="subscribing",
        verbose_name="Автор",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ("user", "author")
        constraints = [
            UniqueConstraint(
                fields=["user", "author"],
                name="unique_subscription"
            )
        ]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

        def __str__(self):
            return f"{self.user} подписан на {self.author}"

        def clean(self):
            if self.user == self.author:
                raise ValidationError("Нельзя подписаться на себя")
