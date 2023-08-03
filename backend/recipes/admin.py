from django.contrib import admin
from django.contrib.admin import display
from rest_framework.exceptions import ValidationError

from .models import (Favourites, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


class RecipeIngredientAdmin(admin.StackedInline):
    model = RecipeIngredient
    autocomplete_fields = ('ingredient',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "id",
        "author",
        "added_in_favorites",
        "get_ingredients"
    )
    readonly_fields = ("added_in_favorites",)
    list_filter = (
        "author",
        "name",
        "tags",
    )
    inlines = (RecipeIngredientAdmin,)

    def save_model(self, request, obj, form, change):
        if not obj.ingredients.exists() or not obj.tags.exists():
            raise ValidationError(
                "Добавьте хотя бы по одному ингредиента и тэга"
            )
        super().save_model(request, obj, form, change)

    @display(description="Количество в избранных")
    def added_in_favorites(self, obj):
        return obj.favorites.count()

    @display(description="Ингредиенты")
    def get_ingredients(self, obj):
        return '\n '.join([
            f'{item["ingredient__name"]} - {item["amount"]}'
            f' {item["ingredient__measurement_unit"]}.'
            for item in obj.recipe.values(
                "ingredient__name",
                "amount", "ingredient__measurement_unit")])


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "measurement_unit",
    )
    search_fields = (
        'name', 'measurement_unit',)
    list_filter = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "color",
        "slug",
    )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
    )


@admin.register(Favourites)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
    )


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        "recipe",
        "ingredient",
        "amount",
    )
