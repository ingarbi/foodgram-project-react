from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscribe, User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "recipes_count",
        "subscribers_count",
    )
    list_filter = ("email", "first_name")

    def recipes_count(self, user):
        return user.recipes.count()

    def subscribers_count(self, user):
        return user.subscriber.count()

    recipes_count.short_description = "Количество рецептов"
    subscribers_count.short_description = "Количество подписчиков"


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "author",
    )
