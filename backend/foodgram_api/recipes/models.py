from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from users.models import User


class Tags(models.Model):
    name_validator = RegexValidator(
        regex=r'^[А-Яа-я]+[^\W\d_]*[А-Яа-я]*$',
        message='Название тега должно'
        'содержать только буквы русского алфавита',
        code='invalid_name'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега',
        unique=True,
        validators=[name_validator]
    )
    slug = models.SlugField(verbose_name='слаг для тега', unique=True)
    color_validator = RegexValidator(
        regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$',
        message='HEX-код цвета должен быть в формате #RRGGBB или #RGB',
        code='invalid_color'
    )
    color = models.CharField(
        max_length=7,
        verbose_name='цвет тега',
        validators=[color_validator]
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    measurement_unit = models.CharField(
        verbose_name='Ед.изм.',
        max_length=10,
        blank=False,
        help_text='Ед. изм.',
        default='шт'
    )
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ('name', )
        verbose_name = "Ингредиенты"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='укажите название рецепта'
    )
    text = models.TextField(verbose_name='Описание рецепта')
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/',
        blank=True
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientInRecipe',
        verbose_name='Ингредиенты',
        help_text='Выберите ингредиенты'
    )
    tags = models.ManyToManyField(
        Tags,
        through='RecipeTags',
        verbose_name='Тег',
        help_text='Теги к рецептам'
    )
    cooking_time = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='время приготовления, мин.',
        help_text='укажите время приготовления в минутах'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        help_text='укажите нужное количество продукта',
        validators=[MinValueValidator(1)]
    )
    recipe = models.ForeignKey(
        Recipes, related_name='ingredientinrecipe',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredients, related_name='ingredientinrecipe',
        on_delete=models.CASCADE,
        verbose_name='ингредиент'
    )

    class Meta:
        verbose_name = 'ингредиены с ед.измерения'
        verbose_name_plural = 'сводная таблица с ед.изм.'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'], name='unique_ingredient')
        ]

    def __str__(self):
        return f'{self.ingredient} - {self.amount}'


class RecipeTags(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE,
                               related_name='recipe_tags')
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE,
                            related_name='recipe_tags')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'tag'],
                                    name='recipe_tag_unique')
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipes, on_delete=models.CASCADE, related_name='favorite',
        verbose_name='Рецепт в избранном',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorite'
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, related_name='shopping_cart',
        on_delete=models.CASCADE
    )

    recipe = models.ForeignKey(
        Recipes,
        related_name='shopping_cart',
        on_delete=models.CASCADE,
        verbose_name='Рецепт в список покупок',
    )

    class Meta:
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_shopping_cart'
            )
        ]


class Subscriptions(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Автор, на которого подписка'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_subscriptions')
        ]

    def __str__(self):
        return f'{self.user} follows {self.author}'
