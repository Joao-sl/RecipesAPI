from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from recipesAPI import views

SITE_NAME = 'receitolas'
app_name = 'recipesAPI'

recipes_api_router = SimpleRouter()


# Admin Recipes
recipes_api_router.register(
    'api/recipes/admin',
    views.AdminRecipesViewSet,
    basename='admin-recipes'
)

# User Recipes
recipes_api_router.register(
    'api/recipes/user',
    views.UserRecipesViewSet,
    basename='user-recipes'
)

# Public Recipes
recipes_api_router.register(
    'api/recipes',
    views.PublicRecipesViewSet,
    basename='public-recipes'
)

# Categories
recipes_api_router.register(
    'api/categories',
    views.GetCategoriesViewSet,
    basename='categories'
)
recipes_api_router.register(
    'api/categories/all',
    views.GetCategoriesViewSet,
    basename='categories-all'
)

# User CRUD
recipes_api_router.register(
    'api/user',
    views.UserViewSet,
    basename='user'
)
urlpatterns = [
    # Django JWT Token
    path(
        'user/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'user/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'user/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),
]

urlpatterns += recipes_api_router.urls
