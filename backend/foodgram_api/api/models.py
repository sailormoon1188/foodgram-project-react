from django.db import models
from foodgram_api.users.models import User


class Recipes(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='укажите название рецепта'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    text = models.TextField()
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        blank=True
    )
    ingredients =
    tags =
    cooking_time = models.PositiveSmallIntegerField(        
        verbose_name='время приготовления, мин.',
        help_text='укажите время приготовления в минутах'
    )
  

    class Meta:
        ordering = ['name']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name