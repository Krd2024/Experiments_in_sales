from .views import TestViewSet, main
from rest_framework.routers import DefaultRouter
from django.urls import include, path


router = DefaultRouter()
router.register(r"tests", TestViewSet, basename="test")

urlpatterns = [
    path("", main, name="main"),
    # path("api/v1/", include(router.urls)),
    path("api/v1/tests/", TestViewSet.as_view()),
]
