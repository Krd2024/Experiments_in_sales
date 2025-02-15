from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import IntegrityError
from django.shortcuts import redirect, render
from loguru import logger

from test_app.serializers import RequestSerializer
from test_app.service.device_service import (
    action_choice_token,
    create_device,
    service_add_devices,
    work_service,
)


def main(request):
    return render(request, "main.html")


def tests(request):
    return render(request, "tests.html")


def work(request):
    context = work_service(request)
    return render(request, "work.html", {"context": context})


class TestViewSet(APIView):

    @extend_schema(
        request=RequestSerializer,
        responses={
            200: {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "device": {"type": "string", "example": "1"},
                        "color": {"type": "string", "example": "#FF0000"},
                        "price": {"type": "number", "example": 10},
                    },
                },
                "example": {"device": "1", "color": "#FF0000", "price": 10},
            }
        },
        operation_id="test_post",
        parameters=[
            OpenApiParameter(
                name="DeviceToken",
                description="Уникальный токен устройства",
                required=True,
                type=str,
                location=OpenApiParameter.HEADER,
            )
        ],
    )
    def post(self, request):
        try:
            # Получить токен из заголовка
            device_token = request.headers.get("DeviceToken")
            # Создать копию
            data = request.data.copy()
            # Добавить токен в запрос
            data["token"] = device_token

            # Прверить наличие устройства в БД
            # При наличии устройства, вернёт из кеша
            data = action_choice_token(device_token)

            if data:

                logger.info((data))
                return Response(data["data"], status=200)

            logger.info((data["message"]))
            return Response({"data": data})

        except IntegrityError as e:
            logger.error(f"Ошибка базы данных: {e}")
            return Response({"error": "Ошибка базы данных"}, status=500)
        except KeyError as e:
            logger.error(f"Отсутствует ключ: {e}")
            return Response({"error": f"Ошибка: отсутствует {str(e)}"}, status=400)
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка",
                e,
            )
            return Response({"error": "Внутренняя ошибка сервера"}, status=500)


def add_devices(request):
    """
    Для тестов
    Вызывает сервисную функцию для добавления устройств
    """

    if request.method == "POST":
        # Получить кол-во устройств для добавления в БД
        number_of_device = request.POST.get("device_count")

        # Получить статистику по устройствам
        context = service_add_devices(request, number_of_device)

        return render(request, "tests.html", {"context": context})

    return redirect("main")
