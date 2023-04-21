import base64

import webcolors
from django.core.files.base import ContentFile
from django.db import transaction
from recipes.models import (IngredientInRecipe, Ingredients, Recipes,
                            RecipeTags, Tags)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .serializers_users import UserSerializer


class Base64ImageField(serializers.ImageField):
    """Поле для кодирования/декодирования цветов в base64."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class Hex2NameColor(serializers.Field):
    """Поле для конвертации цвета в hex-формате."""
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class TagsSerializer(serializers.ModelSerializer):
    """сериализатор тегов."""
    color = Hex2NameColor()

    class Meta:
        model = Tags
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('id', 'name', 'color', 'slug')


class IngredientsSerializer(serializers.ModelSerializer):
    """сериализатор ингредиентов"""
    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор ингердиентов в рецепте
    """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    validators = (
        UniqueTogetherValidator(
            queryset=IngredientInRecipe.objects.all(),
            fields=('ingredient', 'recipe')
        ),
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def __str__(self):
        return f'{self.ingredient} in {self.recipe}'


class AddIngredient(serializers.ModelSerializer):
    """Добавление и редактирование ингредиентов """
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredients.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class AddUpdateRecipesSerializer(serializers.ModelSerializer):
    """Добавление и редактирование рецепта."""

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tags.objects.all())
    ingredients = AddIngredient(many=True)
    image = Base64ImageField(required=False, allow_null=True, use_url=True)

    def validate(self, data):
        """Валидация ингредиентов и тегов."""
        ingredients = data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                'Добавьте ингрелиенты в рецепт'
            )
        unique_ingredients = []
        for item in ingredients:
            name_ingredient = item.get('id')
            amount = item.get('amount')

            if not amount:
                raise serializers.ValidationError(
                    f'Не указано количество для {name_ingredient}'
                )
            if int(amount) <= 0:
                raise serializers.ValidationError(
                    f'Не корректное количество для {name_ingredient}'
                )
            if not isinstance(amount, int):
                raise serializers.ValidationError(
                    'Количество ингредиентов должно быть целым числом'
                )
            if name_ingredient not in unique_ingredients:
                unique_ingredients.append(name_ingredient)
            else:
                raise serializers.ValidationError(
                    'В рецепте не может быть повторяющихся ингредиентов'
                )

        tags = data.get('tags')
        if not tags:
            raise serializers.ValidationError(
                'добавьте тег рецепта'
            )
        if self.instance:
            queryset = Recipes.objects.exclude(pk=self.instance.pk)
        else:
            queryset = Recipes.objects.all()
        if queryset.filter(
            name=data['name']
        ).exists():
            raise serializers.ValidationError(
                'Рецепт уже существует.')
        return data

    def validate_cooking_time(self, cooking_time):
        """Валидация поля времени приготовления."""
        if int(cooking_time) < 1:
            raise serializers.ValidationError(
                'Время приготовления не может быть меньше 1 мин')
        return cooking_time

    def get_ingredients(self, recipe, ingredients):
        ingredient_list = []
        for ingredient in ingredients:
            ingredient_list.append(
                IngredientInRecipe(
                    recipe=recipe,
                    ingredient=ingredient.get('id'),
                    amount=ingredient.get('amount')
                )
            )
        IngredientInRecipe.objects.bulk_create(ingredient_list)

    def get_tags(self, recipe, tags):
        tag_list = []
        for tag in tags:
            tag_list.append(
                RecipeTags(
                    recipe=recipe,
                    tag=tag
                )
            )
        RecipeTags.objects.bulk_create(tag_list)

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipes.objects.create(**validated_data)
        self.get_tags(recipe, tags)
        self.get_ingredients(recipe, ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        IngredientInRecipe.objects.filter(recipe=instance).delete()
        RecipeTags.objects.filter(recipe=instance).delete()
        instance = super().update(instance, validated_data)
        self.get_tags(instance, tags)
        self.get_ingredients(instance, ingredients)
        return instance

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return RecipesListSerializer(instance, context=context).data

    class Meta:
        model = Recipes
        fields = (
            'tags',
            'name',
            'ingredients',
            'image',
            'text',
            'cooking_time'
        )


class RecipesListSerializer(serializers.ModelSerializer):
    """Получение рецептов: GET, RETRIEVE """

    tags = TagsSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True, use_url=True)
    ingredients = IngredientInRecipeSerializer(read_only=True, many=True,
                                               source='ingredientinrecipe')
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    def get_is_favorited(self, object):
        user = self.context.get('request').user
        return (
            not user.is_anonymous
            and object.favorite.filter(user=user).exists()
        )

    def get_is_in_shopping_cart(self, object):
        user = self.context.get('request').user
        return (
            not user.is_anonymous
            and object.shopping_cart.filter(user=user).exists()
        )

    class Meta:
        model = Recipes
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Отображает краткую информацию о рецепте."""

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')
