from django_filters import rest_framework as filters

from recipesAPI.models import Category


class CategoryFilter(filters.FilterSet):
    category_name = filters.CharFilter(
        field_name='category_name',
        lookup_expr='icontains',
    )

    class Meta:
        model = Category
        fields = []
