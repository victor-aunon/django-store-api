from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api_views

router = DefaultRouter()
router.register("products", api_views.ProductViewSet)

urlpatterns = [
    path("api/", include((router.urls, "api"))),
    path("api/token/", api_views.GetToken.as_view(), name="token"),
]
