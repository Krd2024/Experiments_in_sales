# from rest_framework.routers import DefaultRouter
# from test_app.service.device_service import add_devices
from .views import TestViewSet, main, add_devices, tests, work
from django.urls import path


# router = DefaultRouter()
# router.register(r"tests", TestViewSet, basename="test")

urlpatterns = [
    path("", main, name="main"),
    path("tests/", tests, name="tests"),
    path("work/", work, name="work"),
    path("api/v1/tests/", TestViewSet.as_view()),
    path("add_devices/", add_devices, name="add_devices"),
]
