from rest_framework import serializers

from recipesAPI.models import Category, Ingredient, PreparationSteps, Recipe
from recipesAPI.serializers.common_serializer import StrictPayloadSerializer
from recipesAPI.validators import recipe_validators


class IngredientSerializer(StrictPayloadSerializer):
    name = serializers.CharField(required=True)
    quantity = serializers.CharField(required=True)

    class Meta:
        model = Ingredient
        fields = ['name', 'quantity']


class PreparationStepsSerializer(StrictPayloadSerializer):
    step = serializers.CharField(required=True)

    class Meta:
        model = PreparationSteps
        fields = ['step',]


class CategorySerializer(StrictPayloadSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'slug']


class RecipeReadSerializer(StrictPayloadSerializer):
    ingredients = IngredientSerializer(read_only=True, many=True)
    preparation_steps = PreparationStepsSerializer(read_only=True, many=True)
    categories = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'preparation_time', 'ingredients', 'preparation_steps',
            'servings', 'categories', 'slug', 'author', 'tips', 'public', 'admin_approved',
            'approved_by', 'created_at', 'updated_at', 'cover',
        ]


class RecipeWriteSerializer(StrictPayloadSerializer):
    ingredients = serializers.JSONField(write_only=True)
    preparation_steps = serializers.JSONField(write_only=True)
    categories = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )

    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'preparation_time', 'ingredients', 'preparation_steps',
            'servings', 'categories', 'tips', 'cover',
        ]

    def validate_title(self, value):
        return recipe_validators.title_validator(value)

    def validate_ingredients_data(self, value):
        recipe_validators.has_value(value)
        serializer = IngredientSerializer(data=value, many=True)
        serializer.is_valid(raise_exception=True)

        return serializer.validated_data

    def validate_preparation_steps_data(self, value):
        recipe_validators.has_value(value)
        serializer = PreparationStepsSerializer(data=value, many=True)
        serializer.is_valid(raise_exception=True)

        return serializer.validated_data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        preparation_steps = validated_data.pop('preparation_steps', None)
        categories_ids = validated_data.pop('categories', None)

        recipe = Recipe.objects.create(**validated_data)

        for ing in ingredients:
            Ingredient.objects.create(recipe=recipe, **ing)

        for step in preparation_steps:
            PreparationSteps.objects.create(recipe=recipe, **step)

        if categories_ids:
            categories = Category.objects.filter(id__in=categories_ids)
            recipe.categories.set(categories)

        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        preparation_steps = validated_data.pop('preparation_steps', None)
        categories_ids = validated_data.pop('categories', None)

        instance = super().update(instance, validated_data)

        if ingredients:
            instance.ingredients.all().delete()
            for ing in ingredients:
                Ingredient.objects.create(recipe=instance, **ing)

        if preparation_steps:
            instance.preparation_steps.all().delete()
            for step in preparation_steps:
                PreparationSteps.objects.create(recipe=instance, **step)

        if categories_ids:
            categories = Category.objects.filter(id__in=categories_ids)
            instance.categories.set(categories)

        return instance


class AdminRecipeWriteSerializer(RecipeWriteSerializer):
    class Meta(RecipeWriteSerializer.Meta):
        fields = list(RecipeWriteSerializer.Meta.fields) + \
            ['public', 'admin_approved']
