from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from recipes.models import Favorite, Ingredients, Quantity
from recipes.models import Recipes, Subscriptions, Tags
from users.models import User


class SubscriptionsSerializer(serializers.ModelSerializer):
    #is_subscribed = 
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    recipe_author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Subscriptions
        fields = ('user', 'recipe_author')
        validators = [
            UniqueTogetherValidator(
                queryset=Subscriptions.objects.all(),
                fields=('user', 'recipe_author'),
                message=("Подписка уже оформлена!")
            )
        ]

    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя!'
            )
        return data
