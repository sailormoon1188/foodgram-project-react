from django.db import models
from users.models import User


class Tags(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=50)   # HEX прописывается в сериализаторе

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    measurement_unit = models.CharField(
        'Ед.изм.',
        max_length=10,
        blank=False,
        help_text='Ед. изм.',
        default='шт'
    )
    name = models.CharField(max_length=200, unique=True)

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
    text = models.TextField()
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        blank=True
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        related_name='recipes',
        verbose_name='ингредиент',
        help_text='ингредиент'
    )
    tags = models.ManyToManyField(
        Tags,
        related_name='recipes',
        verbose_name='Тег',
        help_text='Теги к рецептам'
    )
    cooking_time = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='время приготовления, мин.',
        help_text='укажите время приготовления в минутах'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Quantity(models.Model):
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        help_text='укажите нужное количество продукта'
    )
    recipe = models.ForeignKey(
        Recipes, related_name='quantity',
        on_delete=models.CASCADE
        )
    ingredient = models.ForeignKey(
        Ingredients, related_name='quantity',
        on_delete=models.CASCADE
        )

    class Meta:
        verbose_name = 'Ед.изм.'
        verbose_name_plural = 'Ед.изм.'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'], name='unique_ingredient')
        ]

    def __str__(self):
        return f'{self.ingredient} - {self.quantity}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipes, on_delete=models.CASCADE, related_name='favored_by',
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


class Shopping_cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipes, on_delete=models.CASCADE,
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
        related_name='subscriber',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='recipe_author',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_subscriptions')
        ]
