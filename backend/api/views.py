from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, IngredientInRecipe, Ingredients, Recipes,
                            ShoppingCart, Subscriptions, Tags)
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from users.models import User

from .filters import IngredientsFilter, RecipeFilter
from .paginations import CustomPagination
from .permissions import IsOwnerOrReadOnly
from .serializers.serializers_recipes import (AddUpdateRecipesSerializer,
                                              IngredientsSerializer,
                                              RecipesListSerializer,
                                              TagsSerializer)
from .serializers.serializers_users import (SubscribeSerializer,
                                            SubscriptionSerializer)
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
    pagination_class = CustomPagination
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipesListSerializer
        return AddUpdateRecipesSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied("Вы не можете удалить этот рецепт.")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(permissions.IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self._add_recipe(Favorite, request, pk)
        return self._delete_recipe(Favorite, request, pk)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(permissions.IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self._add_recipe(ShoppingCart, request, pk)
        return self._delete_recipe(ShoppingCart, request, pk)

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


class SubscriptionViewSet(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    pagination_class = CustomPagination
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.follower.all()


class SubscribeView(views.APIView):
    pagination_class = CustomPagination
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        user = self.request.user
        data = {'author': author.id, 'user': user.id}
        serializer = SubscribeSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        user = self.request.user
        subscription = get_object_or_404(
            Subscriptions, user=user, author=author
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
