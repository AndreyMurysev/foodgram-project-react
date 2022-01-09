from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, IngredientsView, RecipeViewSet, TagViews

router_v1 = DefaultRouter()
router_v1.register('users', CustomUserViewSet, basename='users')
router_v1.register('ingredients', IngredientsView, basename='ingredients')
router_v1.register('tags', TagViews, basename='tag_views')
router_v1.register('recipes', RecipeViewSet, basename='recipes_views')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
