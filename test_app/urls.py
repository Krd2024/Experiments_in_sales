from .views import TestViewSet, main, add_devices, tests, work
from django.urls import path


urlpatterns = [
    path("", main, name="main"),
    path("tests/", tests, name="tests"),
    path("work/", work, name="work"),
    path("api/v1/devices/", TestViewSet.as_view()),
    path("add_devices/", add_devices, name="add_devices"),
    # test
]
