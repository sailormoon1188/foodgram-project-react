from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientsViewSet, RecipesViewSet,
                    SubscribeView, SubscriptionViewSet,
                    TagsViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagsViewSet)  # ready
router.register('ingredients', IngredientsViewSet)  # ready
router.register('recipes', RecipesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/subscriptions/', SubscriptionViewSet.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:pk>/subscribe/', SubscribeView.as_view())
]
