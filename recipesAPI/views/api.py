from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet

from recipesAPI.filters import CategoryFilter
from recipesAPI.mixins import AdminApprovalMixin
from recipesAPI.models import Category, Recipe
from recipesAPI.permissions import CanEditOnlyUnprovedRecipes
from recipesAPI.serializers.recipe_serializer import (
    AdminRecipeWriteSerializer, CategorySerializer, RecipeReadSerializer,
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

        headers = self.get_success_headers(read_serializer.data)

        return Response(
            read_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

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
    search_fields = ['title', 'categories__category_name']


class GetCategoriesViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter
    lookup_field = 'slug'

    @action(detail=False, methods=['get'], url_path='all')
    def get_all(self, request):
        categories = self.get_queryset()
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminRecipesViewSet(ModelViewSet, AdminApprovalMixin):
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Recipe.objects.get_all_recipes()  # type: ignore
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return RecipeReadSerializer
        return AdminRecipeWriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(
            author=request.user,
            approved_by=request.user,
            admin_approved=True
        )

        read_serializer = RecipeReadSerializer(
            instance, context=self.get_serializer_context()
        )
        headers = self.get_success_headers(serializer.data)

        return Response(
            read_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        write_serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=partial
        )
        write_serializer.is_valid(raise_exception=True)
        instance_obj = self.get_object()

        instance = self.perform_approval_logic(
            instance_obj,
            write_serializer,
            request.user
        )

        read_serializer = RecipeReadSerializer(
            instance,
            context=self.get_serializer_context()
        )

        return Response(read_serializer.data)


class StatsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        User = get_user_model()
        payload = {
            'recipes_count': Recipe.objects.filter(
                admin_approved=True,
                public=True
            ).count(),
            'category_count': Category.objects.count(),
            'user_count':    User.objects.count(),
        }
        return Response(payload)
