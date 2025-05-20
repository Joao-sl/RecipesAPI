from django.contrib.auth.models import User
from django.db import models
from django_cleanup import cleanup


@cleanup.select
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='profile'
    )
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=60, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    favorite_recipe = models.CharField(max_length=50, blank=True, null=True)

    def get_full_name(self):
        return f'{UserProfile.first_name} {UserProfile.last_name}'


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.category_name


class RecipeManager(models.Manager):
    def get_public(self):
        queryset = self.filter(public=True)\
            .order_by('-id')\
            .prefetch_related('categories', 'ingredients', 'preparation_steps')\
            .select_related('author')
        return queryset

    def get_approved_and_public(self):
        queryset = self.filter(public=True, admin_approved=True)\
            .order_by('-id')\
            .prefetch_related('categories', 'ingredients', 'preparation_steps')\
            .select_related('author')
        return queryset

    def get_user_recipes(self, user):
        queryset = self.filter(author=user)\
            .order_by('-id')\
            .prefetch_related('categories', 'ingredients', 'preparation_steps')\
            .select_related('author')
        return queryset

    def get_all_recipes(self):
        queryset = Recipe.objects.all()\
            .order_by('-id')\
            .prefetch_related('categories', 'ingredients', 'preparation_steps')\
            .select_related('author')
        return queryset


@cleanup.select
class Recipe(models.Model):
    objects = RecipeManager()

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    preparation_time = models.DurationField(
        help_text='Exemple 25 minutes, 00:25:00'
    )
    servings = models.CharField(max_length=25)
    cover = models.ImageField(upload_to='recipe_covers', null=True)
    slug = models.SlugField()
    categories = models.ManyToManyField(Category, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tips = models.TextField(
        blank=True,
        null=True,
        help_text='This is optional'
    )
    author = models.ForeignKey(
        User,
        models.SET_NULL,
        related_name='authored_recipes',
        null=True
    )
    approved_by = models.ForeignKey(
        User,
        models.SET_NULL,
        related_name='approved_recipes',
        blank=True,
        null=True
    )
    admin_approved = models.BooleanField(default=False)
    public = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title


class Ingredient(models.Model):
    name = models.CharField(max_length=50, null=True)
    quantity = models.CharField(
        max_length=50,
        help_text='2 cups, 1 spoon, etc',
        null=True
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredients',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self) -> str:
        return f'{self.name} - {self.quantity}'


class PreparationSteps(models.Model):
    class Meta:
        verbose_name = 'Preparation Step'
        verbose_name_plural = 'Preparation Steps'

    step = models.TextField(
        help_text='Write the step and add another one',
        null=True
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='preparation_steps',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self) -> str:
        return 'Step'
