from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from recipesAPI.models import Category, Ingredient, IngredientsManager, Recipe

UserAdmin.list_display = ['id'] + list(UserAdmin.list_display)
UserAdmin.list_display_links = ['id', 'username']


class IngredientsManagerInline(admin.StackedInline):
    model = IngredientsManager
    extra = 1
    autocomplete_fields = ['ingredient']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientsManagerInline]
    list_display = ['id', 'title', 'description', 'public']
    list_display_links = ['id', 'title']
    readonly_fields = ['created_at', 'updated_at', 'slug']
    search_fields = ['id', 'title', 'description']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'warning']
    list_display_links = ['id', 'name']
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name']
    list_display_links = ['id', 'category_name']
    prepopulated_fields = {'slug': ['category_name']}
    readonly_fields = ['created_at']
    search_fields = ['id', 'category_name']
