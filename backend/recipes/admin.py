from django.contrib import admin

from .models import (Favorite, IngredientInRecipe, Ingredients, Recipes,
                     RecipeTags, ShoppingCart, Subscriptions, Tags)


class QuantityInline(admin.TabularInline):
    model = IngredientInRecipe
    min_num = 1
    extra = 0


class TagsInline(admin.TabularInline):
    model = RecipeTags
    min_num = 1
    extra = 0


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'ingredient',
        'recipe',
        'amount'
    )
    search_fields = ('recipe__name', 'ingredient__name')


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
    inlines = (QuantityInline, TagsInline)
    list_display = (
        'pk',
        'name',
        'author',
        'display_tags',
    )
    list_filter = ('name', 'author', 'tags')
    search_fields = (
        'name',
        'author__username',
        'author__email'
    )
    readonly_fields = ('is_favorited',)

    def is_favorited(self, obj):
        return obj.favorite.count()
    is_favorited.short_description = 'Раз в избранном'

    def display_tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])
    display_tags.short_description = 'Теги'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user', 'recipe', )
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe', )


@admin.register(Subscriptions)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    empty_value_display = '-пусто-'
