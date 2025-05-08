from rest_framework import generics, status

from recipesAPI.models import Recipe
from recipesAPI.serializers.recipe_serializer import GetRecipesSerializer


class GetRecipesView(generics.ListAPIView):
    queryset = Recipe.objects.filter(public=True)
    serializer_class = GetRecipesSerializer
