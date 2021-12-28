import webcolors

from djoser.serializers import UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from users.models import User, Follow
from recipies.models import (Favorite,
                             Ingredient,
                             Recipe,
                             RecipeIngredients,
                             ShoppingCart,
                             Tag,)


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user,
            author=obj.id).exists()


class CustomUserSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'password')


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        try:
            value = webcolors.name_to_hex(value)
        except ValueError:
            raise serializers.ValidationError('Для этого имени нет цвета')
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого имени нет цвета')
        return data


class TagSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'amount', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='recipe_ingredient',
        many=True, read_only=True,)
    is_favorited = serializers.SerializerMethodField(default=False)
    is_in_shopping_cart = serializers.SerializerMethodField(default=False)

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=request.user,
            recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user,
            recipe=obj).exists()

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_set = set()
        for ingredient in ingredients:
            if int(ingredient.get('amount')) <= 0:
                raise serializers.ValidationError(
                    ('Убедитесь, что значение количества '
                     'ингредиента больше 0')
                )
            id = ingredient.get('id')
            if id in ingredients_set:
                raise serializers.ValidationError(
                    'Ингредиент в рецепте не должен повторяться.'
                )
            ingredients_set.add(id)
        data['ingredients'] = ingredients
        return data

    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients = validated_data.pop('ingredients')
        tags = self.initial_data.get('tags')
        recipe = Recipe.objects.create(image=image, **validated_data)
        for tag_id in tags:
            recipe.tags.add(get_object_or_404(Tag, pk=tag_id))
        for ingredient in ingredients:
            RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'))
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        tags = self.initial_data.get('tags')
        for tag_id in tags:
            instance.tags.add(get_object_or_404(Tag, pk=tag_id))
        RecipeIngredients.objects.filter(recipe=instance).delete()
        for ingredient in validated_data.get('ingredients'):
            ingredients_amounts = RecipeIngredients.objects.create(
                recipe=instance,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'))
            ingredients_amounts.save()
        if validated_data.get('image') is not None:
            instance.image = validated_data.get('image')
        instance.name = validated_data.get('name')
        instance.text = validated_data.get('text')
        instance.cooking_time = validated_data.get('cooking_time')
        instance.save()
        return instance


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True)
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        write_only=True)
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.SerializerMethodField()
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time', 'user', 'recipe')

    def get_image(self, obj):
        request = self.context.get('request')
        photo_url = obj.recipe.image.url
        return request.build_absolute_uri(photo_url)

    def validate(self, data):
        request = self.context.get('request')
        recipe_id = data['recipe'].id
        favorite = Favorite.objects.filter(
                    user=request.user,
                    recipe__id=recipe_id
                ).exists()
        if request.method == 'GET':
            if request.user.is_anonymous:
                raise serializers.ValidationError(
                    'Учетные данные не предоставлены'
                )
            if favorite:
                raise serializers.ValidationError(
                    'Рецепт уже есть в избранном'
                )
        if request.method == 'DELETE':
            if not favorite:
                raise serializers.ValidationError(
                    'Рецепта нет в избранном'
                )
        return data


class RecipeAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True)
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True)
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    recipes = RecipeAuthorSerializer(
        source='author.recipe',
        many=True, read_only=True)

    class Meta:
        model = Follow
        fields = ('id',
                  'email',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  'recipes',
                  'recipes_count',
                  'user',
                  'author')

    def validate(self, data):
        request = self.context.get('request')
        author_id = data['author'].id
        follow = Follow.objects.filter(
                    user=request.user,
                    author__id=author_id
                ).exists()
        if request.method == 'GET':
            if request.user.id == author_id:
                raise serializers.ValidationError(
                    'Невозможно подписаться на себя'
                )
            if follow:
                raise serializers.ValidationError(
                    'Подписан на этого пользователя'
                )
        if request.method == 'DELETE':
            if not follow:
                raise serializers.ValidationError(
                    'Вы не подписаны на этого пользователя'
                )
        return data

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=obj.user,
                                     author=obj.author).exists()

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True)
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        write_only=True)
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.SerializerMethodField()
    cooking_time = serializers.ReadOnlyField(
        source='recipe.cooking_time')

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time', 'user', 'recipe')

    def get_image(self, obj):
        request = self.context.get('request')
        photo_url = obj.recipe.image.url
        return request.build_absolute_uri(photo_url)

    def validate(self, data):
        request = self.context.get('request')
        recipe_id = data['recipe'].id
        shopping_cart = ShoppingCart.objects.filter(
            user=request.user,
            recipe__id=recipe_id).exists()
        if request.method == 'GET':
            if request.user.is_anonymous:
                raise serializers.ValidationError(
                    'Учетные данные не предоставлены')
            if shopping_cart:
                raise serializers.ValidationError(
                    'Рецепт уже есть в списке покупок')
        if request.method == 'DELETE':
            if not shopping_cart:
                raise serializers.ValidationError(
                    'Рецепта нет в списке покупок')
        return data
