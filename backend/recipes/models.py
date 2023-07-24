from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField("Название", max_length=200)
    measurement_unit = models.CharField(
        "Единица измерения ингредиента", max_length=200)

    class Meta:
        ordering = ["name"]
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f"{self.name}, {self.measurement_unit}"


class Tag(models.Model):
    name = models.CharField("Название", unique=True, max_length=200)
    color = models.CharField(
        "Цвет HEX-кода",
        unique=True,
        max_length=7,
        validators=[
            RegexValidator(
                regex="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
                message="Введенное значение не является цветом в формате HEX!",
            )
        ],
    )
    slug = models.SlugField("Ссылка", unique=True, max_length=200)

    class Meta:
        ordering = ["-id"]
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
    name = models.CharField("Название рецепта", max_length=200)
    text = models.TextField("Описание рецепта")
    image = models.ImageField("Изображение рецепта", upload_to="recipes/")
    cooking_time = models.PositiveSmallIntegerField(
        "Время приготовления",
        validators=[MinValueValidator(
            1, message="Минимальное значение 1 минута!")],
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        related_name="recipes",
        verbose_name="Ингредиенты",
    )
    tags = models.ManyToManyField(
        Tag, related_name="recipes", verbose_name="Теги")

    class Meta:
        ordering = ["-id"]
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
        "Количество",
        validators=[
            MinValueValidator(
                1, message="Минимальное количество ингридиентов 1!")
        ],
    )

    class Meta:
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецептах"
        ordering = ["-id"]
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


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Рецепт",
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        constraints = [
            UniqueConstraint(fields=["user", "recipe"],
                             name="unique_favourite")
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Избранное'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        verbose_name="Рецепт",
    )

    class Meta:
        verbose_name = "Корзина покупок"
        verbose_name_plural = "Корзина покупок"
        ordering = ["-id"]
        constraints = [
            UniqueConstraint(fields=["user", "recipe"],
                             name="unique_shopping_cart")
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Корзину покупок'
