from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientsViewSet, RecipesViewSet, SubscribeView,
                    SubscriptionViewSet, TagsViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)
router.register('recipes', RecipesViewSet)

users_urls = [
    path('subscriptions/', SubscriptionViewSet.as_view()),
    path('<int:pk>/subscribe/', SubscribeView.as_view())
]

djoser_urls = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

urlpatterns = [
    path('', include(router.urls)),
    path('users/', include(users_urls)),
    *djoser_urls,
]
