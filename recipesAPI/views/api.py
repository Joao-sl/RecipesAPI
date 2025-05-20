from rest_framework import generics, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipesAPI.filters import CategoryFilter
from recipesAPI.models import Category, Recipe
from recipesAPI.permissions import CanEditOnlyUnprovedRecipes
from recipesAPI.serializers.recipe_serializer import (CategorySerializer,
                                                      RecipeReadSerializer,
                                                      RecipeWriteSerializer)


class UserRecipesViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, CanEditOnlyUnprovedRecipes]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    http_method_names = ['get', 'post', 'patch', 'delete']
    lookup_field = 'slug'
    search_fields = 'title',

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def get_queryset(self):
        user = self.request.user
        return Recipe.objects.get_user_recipes(user)  # type: ignore

    def create(self, request, *args, **kwargs):
        write_serializer = self.get_serializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        instance = write_serializer.save(author=request.user)

        read_serializer = RecipeReadSerializer(
            instance,
            context=self.get_serializer_context()
        )
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        write_serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=partial
        )
        write_serializer.is_valid(raise_exception=True)
        instance = write_serializer.save()

        read_serializer = RecipeReadSerializer(
            instance,
            context=self.get_serializer_context()
        )
        return Response(read_serializer.data)


class PublicRecipesViewSet(ReadOnlyModelViewSet):
    queryset = Recipe.objects.get_approved_and_public()  # type: ignore
    permission_classes = [AllowAny]
    serializer_class = RecipeReadSerializer
    http_method_names = ['get']
    lookup_field = 'slug'
    search_fields = ['title']


class GetCategoriesViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter
    lookup_field = 'slug'
