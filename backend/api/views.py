import io

from django.conf import settings
from django.db.models import Exists, OuterRef
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser import views
from recipies.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from reportlab import rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import Follow, User

from .filters import RecipeFilter
from .paginations import CustomPagination
from .permissions import EditAuthorAndAdminOrReadAll
from .serializers import (FavoriteRecipeSerializer, FollowSerializer,
                          IngredientsSerializer, RecipeSerializer,
                          ShoppingCartSerializer, TagSerializer,
                          UserSerializer)

rl_config.TTFSearchPath.append(
    str(settings.BASE_DIR) + '/lib/reportlabs/fonts/')


class CustomUserViewSet(views.UserViewSet):
    queryset = User.objects.all()
    permission_classes = (EditAuthorAndAdminOrReadAll,)
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True,
            methods=['GET', 'DELETE'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = get_object_or_404(User, username=request.user.username)
        author = get_object_or_404(User, id=id)
        data = {
            'user': user.id,
            'author': author.id,
        }
        serializer = FollowSerializer(
            data=data, context={'request': request})
        if request.method == 'GET' and serializer.is_valid(
                raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        serializer.is_valid(raise_exception=True)
        follow = get_object_or_404(Follow, user=user, author=author)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientsView(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    permission_classes = (AllowAny,)


class TagViews(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (EditAuthorAndAdminOrReadAll,)
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filter_class = RecipeFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Recipe.objects.all()
        queryset = Recipe.objects.annotate(
            is_favorited=Exists(Favorite.objects.filter(
                user=user, recipe_id=OuterRef('pk'))),
            is_in_shopping_cart=Exists(ShoppingCart.objects.filter(
                user=user, recipe_id=OuterRef('pk'))))
        if self.request.GET.get('is_favorited'):
            return queryset.filter(is_favorited=True)
        elif self.request.GET.get('is_in_shopping_cart'):
            return queryset.filter(is_in_shopping_cart=True)

        return queryset

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(detail=True,
            methods=['GET', 'DELETE'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        user = get_object_or_404(User, username=request.user.username)
        recipe = get_object_or_404(Recipe, pk=pk)
        data = {
            'user': user.id,
            'recipe': recipe.id}
        serializer = FavoriteRecipeSerializer(
            data=data, context={'request': request})
        if request.method == 'GET' and serializer.is_valid(
                raise_exception=True):
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED)
        serializer.is_valid(raise_exception=True)
        favorite = get_object_or_404(Favorite,
                                     user=user,
                                     recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['GET', 'DELETE'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        user = get_object_or_404(User, username=request.user.username)
        recipe = get_object_or_404(Recipe, pk=pk)
        data = {
            'user': user.id,
            'recipe': recipe.id}
        serializer = ShoppingCartSerializer(
            data=data, context={'request': request})
        if request.method == 'GET' and serializer.is_valid(
                raise_exception=True):
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED)
        serializer.is_valid(raise_exception=True)
        favorite = get_object_or_404(ShoppingCart,
                                     user=user,
                                     recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=['GET'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = get_object_or_404(User, username=request.user.username)
        shopping_cart = user.shopping_user.all()
        dict = {}
        for num in shopping_cart:
            ingredients_list = num.recipe.recipe_ingredient.all()
            for ingredient in ingredients_list:
                name = ingredient.ingredient.name
                amount = ingredient.amount
                measurement_unit = ingredient.ingredient.measurement_unit
                if name not in dict:
                    dict[name] = {
                        'measurement_unit': measurement_unit,
                        'amount': amount}
                else:
                    dict[name]['amount'] = (dict[name]['amount'] + amount)
        list = []
        i = 0
        for key in dict:
            i += 1
            list.append(f'{i}. {key} - {dict[key]["amount"]} - '
                        f'{dict[key]["measurement_unit"]}')
        buffer = io.BytesIO()
        pdfmetrics.registerFont(TTFont('TNRB', 'timesbd.ttf'))
        p = canvas.Canvas(buffer)
        p.setFont('TNRB', 16)
        x = 0
        for int in range(len(list)):
            x = x + 20
            p.drawString(20, 727 - x, list[int])
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='canvas.pdf')
