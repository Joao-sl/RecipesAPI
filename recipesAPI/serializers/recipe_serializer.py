from rest_framework import serializers

from recipesAPI.models import Ingredient, IngredientsManager, Recipe


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name',]


class IngredientThroughSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientsManager
        fields = ['ingredient', 'quantity',]

    ingredient = IngredientSerializer()


class GetRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'preparation_time', 'ingredients', 'preparation_steps',
                  'servings', 'slug', 'category', 'tips', 'author', 'created_at', 'updated_at', 'cover',]

    ingredients = IngredientThroughSerializer(
        many=True, source='ingredientsmanager_set')
