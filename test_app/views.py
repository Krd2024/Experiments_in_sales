from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import IntegrityError
from django.shortcuts import redirect, render
from loguru import logger

# from test_app.service.config import action_choice_token, service_add_devices
from test_app.serializers import DeviceSerializer, RequestSerializer
from test_app.service.device_service import action_choice_token, service_add_devices


def main(request):
    return render(request, "main.html")


class TestViewSet(APIView):
    def get_serializer_class(self):
        if self.request.method == "POST":
            return DeviceSerializer
        return DeviceSerializer

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
            # Получить сериалайзер
            serializer = self.get_serializer_class()(data=data)

            data = action_choice_token(device_token)
            logger.info((f"✅ {data} < --- Данные из кеша "))

            if data:
                return Response(data, status=200)

            if serializer.is_valid():
                data = serializer.data["token"]
                logger.info((f"✅ {data} < --- Новые данные"))
                return Response({"data": data})

            logger.error(serializer.errors)
            return Response(serializer.errors, status=400)

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
    if request.method == "POST":
        number_of_device = request.POST.get("device_count")
        logger.debug(number_of_device)

        context = service_add_devices(request, number_of_device)

        # logger.info(context)
        return render(request, "main.html", {"context": context})

    return redirect("main")
