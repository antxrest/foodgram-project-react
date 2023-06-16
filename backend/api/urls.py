from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    FollowViewSet,
    IngredientsViewSet,
    RecipesViewSet,
    TagsViewSet,
)

app_name = "api"

router_v1 = DefaultRouter()
router_v1.register("users", FollowViewSet)
router_v1.register("recipes", RecipesViewSet, basename="recipes")
router_v1.register("tags", TagsViewSet)
router_v1.register("ingredients", IngredientsViewSet)

urlpatterns = [
    path("", include(router_v1.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
