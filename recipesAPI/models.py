from django.contrib.auth.models import User
from django.db import models
from django_cleanup import cleanup


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.category_name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text='BE CAREFUL WHEN YOU EDITING INGREDIENT NAME, IT WILL BE EDITED IN ALL RECIPES ON THE SITE'
    )
    warning = models.CharField(
        max_length=150,
        editable=False,
        default='BE CAREFUL WHEN YOU EDITING INGREDIENT NAME, IT WILL BE EDITED IN ALL RECIPES ON THE SITE'
    )

    def __str__(self) -> str:
        return self.name


@cleanup.select
class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    preparation_time = models.DurationField(
        help_text='Exemple 25 minutes, 00:25:00',
        null=True
    )
    servings = models.CharField(max_length=25, null=True)
    cover = models.ImageField(upload_to='recipe_covers', null=True)
    slug = models.SlugField(null=True)
    category = models.ForeignKey(Category, models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    preparation_steps = models.TextField(null=True)
    tips = models.TextField(
        blank=True,
        null=True,
        help_text='This is optional'
    )
    author = models.ForeignKey(User, models.SET_NULL, null=True)
    public = models.BooleanField(default=False)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsManager'
    )

    def __str__(self) -> str:
        return self.title


class IngredientsManager(models.Model):
    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(
        max_length=50, help_text='2 cups, 1 spoon, etc')

    def __str__(self) -> str:
        return f'{self.quantity} of {self.ingredient}'
