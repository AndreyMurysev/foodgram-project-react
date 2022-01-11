from django.db import models
from users.models import User

COLOR = [
    ('yellow', 'желтый'),
    ('green', 'зеленый'),
    ('blue', 'синий'),
    ('brown', 'коричневый'),
    ('white', 'белый'),
    ('red', 'красный'),
    ('orange', 'оранжевый'),
    ('pink', 'розовый')]

MESURMENT_UNIT = [
    ('г', 'г'),
    ('стакан', 'стакан'),
    ('по вкусу', 'по вкусу'),
    ('ст. л.', 'ст. л.'),
    ('шт.', 'шт.'),
    ('мл', 'мл'),
    ('ч. л.', 'ч. л.'),
    ('капля', 'капля'),
    ('звездочка', 'звездочка'),
    ('щепотка', 'щепотка'),
    ('горсть', 'горсть'),
    ('кусок', 'кусок'),
    ('кг', 'кг'),
    ('пакет', 'пакет'),
    ('пучок', 'пучок'),
    ('долька', 'долька'),
    ('банка', 'банка'),
    ('упаковка', 'упаковка'),
    ('зубчик', 'зубчик'),
    ('пласт', 'пласт'),
    ('пачка', 'пачка'),
    ('тушка', 'тушка'),
    ('стручок', 'стручок'),
    ('веточка', 'веточка'),
    ('бутылка', 'бутылка'),
    ('л', 'л'),
    ('пакетик', 'пакетик'),
    ('лист', 'лист'),
    ('стебель', 'стебель')]


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        blank=False,
        unique=True)
    slug = models.SlugField(
        max_length=200,
        verbose_name='Адрес',
        blank=False,
        unique=True)
    color = models.CharField(
        max_length=7,
        choices=COLOR,
        verbose_name='Цвет',
        blank=False,
        unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.name}'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='Наименование',
        blank=False)
    measurement_unit = models.CharField(
        max_length=15,
        choices=MESURMENT_UNIT,
        verbose_name='Единица измерения',
        blank=False)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    name = models.CharField('Наименование', max_length=200)
    text = models.TextField('Текст')
    cooking_time = models.PositiveSmallIntegerField('Время приготовления')
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор',)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredients',
        verbose_name='Ингредиенты',)
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='tag_recipes',)
    date_pub = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-date_pub',)
        constraints = (
            models.CheckConstraint(
                check=models.Q(cooking_time__gte=1),
                name='time_gte_1'),)

    def __str__(self):
        return f'{self.name}'


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient',
        verbose_name='Рецепт',)
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_recipe',
        verbose_name='Ингредиент',)
    amount = models.PositiveIntegerField('Количество')

    class Meta:
        ordering = ('-id',)
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient',),
                name='unique_ingred_recipe'),
            models.CheckConstraint(
                check=models.Q(amount__gte=1),
                name='amount_gte_1'),)

    def __str__(self):
        return f'{self.ingredient}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_user',
        verbose_name='Пользователь',)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='Рецепт',)

    class Meta:
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранное'
        ordering = ('-id',)
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_favorite'),)

    def __str__(self):
        return f'{self.user}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_user',
        verbose_name='Пользователь',)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_recipe',
        verbose_name='Рецепт',)

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        ordering = ('-id',)
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_shop'),)

    def __str__(self):
        return f'{self.recipe}'
