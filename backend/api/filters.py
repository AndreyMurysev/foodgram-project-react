import django_filters as filters

from users.models import User
from recipies.models import Recipe


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug')
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all())

    class Meta:
        model = Recipe
        fields = ['tags', 'author']
