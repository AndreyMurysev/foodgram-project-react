import django_filters as filters
from recipies.models import Recipe
from users.models import User


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug')
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all())

    class Meta:
        model = Recipe
        fields = ['tags', 'author']
