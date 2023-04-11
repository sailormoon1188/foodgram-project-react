from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientsViewSet, RecipesViewSet, TagsViewSet,
                    UsersViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagsViewSet)  # ready
router.register('ingredients', IngredientsViewSet)  # ready
router.register('recipes', RecipesViewSet)
router.register(r'users', UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
