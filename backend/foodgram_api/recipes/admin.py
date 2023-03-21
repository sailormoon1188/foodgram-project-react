from django.contrib import admin

from .models import Ingredients, Quantity, Recipes, Tags


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name', )
    list_filter = ('name', )
    empty_value_display = '-пусто-'
    list_editable = ('name', 'measurement_unit')


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'color')
    search_fields = ('name', )
    empty_value_display = '-пусто-'
    list_editable = ('name', 'slug', 'color')


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'text', 'image',
                    'cooking_time')
    search_fields = ('name', 'author')
    list_filter = ('tags', )
    empty_value_display = '-пусто-'
    list_editable = ('name', 'text')


@admin.register(Quantity)
class QuantityAdmin(admin.ModelAdmin):
    list_display = ('pk', 'quantity', 'recipe', 'ingredient')
    list_filter = ('recipe',)
    empty_value_display = '-пусто-'
