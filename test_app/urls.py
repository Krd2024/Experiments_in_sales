# from rest_framework.routers import DefaultRouter
from .views import TestViewSet, main
from django.urls import path


# router = DefaultRouter()
# router.register(r"tests", TestViewSet, basename="test")

urlpatterns = [
    path("", main, name="main"),
    path("api/v1/tests/", TestViewSet.as_view()),
]
