from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from recipesAPI.models import Category, Ingredient, PreparationSteps, Recipe

UserAdmin.list_display = ['id'] + list(UserAdmin.list_display)
UserAdmin.list_display_links = ['id', 'username']


class IngredientTabularInline(admin.TabularInline):
    model = Ingredient
    extra = 1


class PreparationStepsInline(admin.TabularInline):
    model = PreparationSteps
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientTabularInline, PreparationStepsInline]
    list_display = ['id', 'title', 'description', 'admin_approved', 'public']
    list_display_links = ['id', 'title']
    # list_editable = ['public']
    readonly_fields = ['created_at', 'updated_at', 'slug']
    search_fields = ['id', 'title', 'description']
    autocomplete_fields = ['categories']

    # Only staff users
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "approved_by":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name']
    list_display_links = ['id', 'category_name']
    prepopulated_fields = {'slug': ['category_name']}
    readonly_fields = ['created_at']
    search_fields = ['id', 'category_name']
    ordering = ['-id']
