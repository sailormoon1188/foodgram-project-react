from django.db.models import Sum
from django.forms import ValidationError
from djoser.views import UserViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .filters import IngredientsFilter, RecipeFilter
from recipes.models import (Favorite, Ingredients,
                            IngredientInRecipe, Recipes,
                            ShoppingCart, Tags)
from .permissions import (IsOwnerOrReadOnly)

from .serializers.serializers_reviews import (
     AddUpdateRecipesSerializer, IngredientsSerializer,
     RecipesListSerializer, ShortRecipeSerializer,
     TagsSerializer
)
from .utils import convert_txt


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для  тегов: ReadOnly."""
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (permissions.AllowAny, )
    pagination_class = None


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для  рецептов: ReadOnly."""
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (permissions.AllowAny, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientsFilter
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    """Вьюсет для  рецептов.
       Action-функционал: избранное и список покупок.
    """
    queryset = Recipes.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipesListSerializer
        return AddUpdateRecipesSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def add_recipe(self, model, request, pk):
        recipe = get_object_or_404(Recipes, pk=pk)
        user = self.request.user
        if model.objects.filter(recipe=recipe, user=user).exists():
            raise ValidationError('Рецепт уже добавлен')
        model.objects.create(recipe=recipe, user=user)
        serializer = ShortRecipeSerializer(recipe)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete_recipe(self, model, request, pk):
        recipe = get_object_or_404(Recipes, pk=pk)
        user = self.request.user
        obj = get_object_or_404(model, recipe=recipe, user=user)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(permissions.IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.add_recipe(Favorite, request, pk)
        else:
            return self.delete_recipe(Favorite, request, pk)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(permissions.IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_recipe(ShoppingCart, request, pk)
        else:
            return self.delete_recipe(ShoppingCart, request, pk)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=(IsOwnerOrReadOnly, ),
        pagination_class=None
    )
    def download_shopping_cart(self, request):
        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).order_by(
            'ingredient__name'
        ).annotate(ingredient_total=Sum('amount'))
        return convert_txt(ingredients)


class UsersViewSet(UserViewSet):
    """Вьюсет для работы с пользователями и подписками.
    Обработка запросов на создание/получение пользователей и
    создание/получение/удаления подписок."""
    