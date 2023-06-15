from django.urls import include, path
from rest_framework import routers

from api.views import (
    IngredientsViewSet,
    TagsViewSet,
    FollowView,
    FollowUserView,
    RecipesViewSet
)

app_name = 'api'

router = routers.DefaultRouter()
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path('users/subscriptions/', FollowView.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('users/<int:id>/subscribe/', FollowUserView.as_view()),
]
