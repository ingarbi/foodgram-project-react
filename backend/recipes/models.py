from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.constants import (HEX_LENGHT, MAX_COOKING_TIME, MAX_INGREDIENTS,
                           MAX_LENGTH, MIN_COOKING_TIME, MIN_INGREDIENTS)
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(verbose_name="Название", max_length=MAX_LENGTH)
    measurement_unit = models.CharField(
        verbose_name="Единица измерения ингредиента",
        max_length=MAX_LENGTH
    )

    class Meta:
        ordering = ("name", "measurement_unit")
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "measurement_unit"],
                name="unique ingredient name"
            )
        ]

    def __str__(self):
        return f"{self.name}, {self.measurement_unit}"


class Tag(models.Model):
    name = models.CharField(
        verbose_name="Название",
        unique=True,
        max_length=MAX_LENGTH
    )
    color = ColorField(
        verbose_name="Цвет HEX-кода",
        unique=True,
        max_length=HEX_LENGHT,
        default='#FF0000'
    )
    slug = models.SlugField(
        verbose_name="Ссылка",
        unique=True,
        max_length=MAX_LENGTH
    )

    class Meta:
        ordering = ("name", "slug")
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name="recipes",
        on_delete=models.CASCADE,
        verbose_name="Автор рецепта",
    )
    name = models.CharField(
        verbose_name="Название рецепта",
        max_length=MAX_LENGTH
    )
    text = models.TextField(verbose_name="Описание рецепта")
    image = models.ImageField(
        verbose_name="Изображение рецепта", upload_to="recipes/"
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления",
        validators=[
            MinValueValidator(
                MIN_COOKING_TIME, message="Минимальное значение 1 минута!"
            ),
            MaxValueValidator(
                MAX_COOKING_TIME, message="Максимальное значение 2 часа!"
            )
        ],
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        related_name="recipes",
        verbose_name="Ингредиенты",
    )
    tags = models.ManyToManyField(
        Tag, related_name="recipes", verbose_name="Теги")
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)

    class Meta:
        ordering = ("name", "author", "cooking_time")
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент",
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество",
        validators=[
            MinValueValidator(
                MIN_INGREDIENTS,
                message="Минимальное количество ингридиентов 1!"
            ),
            MaxValueValidator(
                MAX_INGREDIENTS,
                message="Максимальное количество ингридиентов 100!"
            )
        ],
    )

    class Meta:
        ordering = ("recipe", "ingredient", "amount")
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецептах"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique ingredient"
            )
        ]

    def __str__(self):
        return (
            f"{self.ingredient.name} ({self.ingredient.measurement_unit})"
            f" - {self.amount} "
        )


class FavouriteShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s',
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='%(class)s',
        verbose_name="Рецепт",
    )

    class Meta:
        abstract = True


class Favourites(FavouriteShoppingCart):

    class Meta:
        ordering = ("user", "recipe")
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        constraints = [
            UniqueConstraint(fields=["user", "recipe"],
                             name="unique_favourite")
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Избранное'


class ShoppingCart(FavouriteShoppingCart):

    class Meta:
        ordering = ("user", "recipe")
        verbose_name = "Корзина покупок"
        verbose_name_plural = "Корзина покупок"
        constraints = [
            UniqueConstraint(fields=["user", "recipe"],
                             name="unique_shopping_cart")
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Корзину покупок'
