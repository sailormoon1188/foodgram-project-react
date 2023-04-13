from django.forms import ValidationError
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from recipes.models import Recipes
from users.models import User
from recipes.models import Subscriptions
#from .serializers_recipes import ShortRecipeSerializer


class MyUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для обработки запросов на создание пользователя.
    Валидирует создание пользователя с юзернеймом 'me'."""

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )

    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise ValidationError(
                'Пользователь с таким email уже зарегистрирован'
            )
        return lower_email

    def validate_username(self, value):
        lower_username = value.lower()
        if User.objects.filter(username__iexact=lower_username).exists():
            raise ValidationError(
                'Пользователь с таким username уже зарегистрирован'
            )
        if value == "me":
            raise ValidationError(
                'Невозможно создать пользователя с таким именем!'
            )
        return lower_username


class MyUserSerializer(UserSerializer):

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscriptions.objects.filter(
            user=request.user, author=obj
        ).exists()



class ShortRecipeSerializer(serializers.ModelSerializer):
    """Отображает краткую информацию о рецепте."""

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')



class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscriptions
        fields = ('user', 'author')

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        serializer = SubscriptionSerializer(
            instance,
            context=context
        )
        return serializer.data

    def validate(self, data):
        user = data.get('user')
        author = data.get('author')
        if user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        if Subscriptions.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя!'
            )
        return data


class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )
    recipes = serializers.SerializerMethodField(method_name='get_recipes')
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )

    class Meta:
        model = Subscriptions
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return Subscriptions.objects.filter(
            author=obj.author, user=request.user
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        if request.GET.get('recipe_limit'):
            recipe_limit = int(request.GET.get('recipe_limit'))
            queryset = Recipes.objects.filter(
                author=obj.author)[:recipe_limit]
        else:
            queryset = Recipes.objects.filter(
                author=obj.author)

        serializer = ShortRecipeSerializer(
            queryset, read_only=True, many=True
        )
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()
