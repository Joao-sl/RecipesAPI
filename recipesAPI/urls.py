from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from recipesAPI import views

SITE_NAME = 'receitolas'
app_name = 'recipes'

urlpatterns = [
    # Recipes
    path("recipes/", views.GetRecipesView.as_view(), name='recipes'),

    # User CRUD
    path(
        "user/register/",
        views.UserRegisterView.as_view(),
        name='register'
    ),
    path(
        "user/read/<int:pk>",
        views.GetUserView.as_view(),
        name='get_user'
    ),
    path(
        "user/edit_profile/<int:pk>",
        views.ProfileUserUpdate.as_view(),
        name='edit_profile'
    ),
    path(
        "user/edit_account/<int:pk>",
        views.SecurityUserUpdate.as_view(),
        name='edit_account'),
    path(
        "user/delete/<int:pk>",
        views.DeleteUserView.as_view(),
        name='delete'
    ),

    # Django JWT Token
    path(
        'recipes/api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'recipes/api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'recipes/api/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),
]
