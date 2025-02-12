from django.db import IntegrityError
from django.shortcuts import render
from loguru import logger
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# from .serializers import TestSerializer
from test_app.serializers import DeviceSerializer
from test_app.service.device_service import action_choice_token, cache_price


def main(request):
    return render(request, "main.html")


class TestViewSet(APIView):
    def get_serializer_class(self):
        if self.request.method == "POST":
            return DeviceSerializer
        return DeviceSerializer

    def get(self, request):
        serializer = self.get_serializer_class()()
        return Response({"message": "GET request", "schema": serializer.data})

    @extend_schema(
        operation_id="test_post",
        parameters=[
            OpenApiParameter(
                name="Device-Token",
                description="Уникальный токен устройства",
                required=True,
                type=str,
                location=OpenApiParameter.HEADER,
            )
        ],
        # request=DeviceSerializer,
    )
    def post(self, request):
        try:
            # Получить токен из заголовка
            device_token = request.headers.get("Device-Token")
            # Создать копию
            data = request.data.copy()
            # Добавить токен в запрос
            data["token"] = device_token
            # Получить сериалайзер
            serializer = self.get_serializer_class()(data=data)

            data = action_choice_token(device_token)
            logger.info((f"✅ {data} < ----------- Данные из кеша "))

            if data:
                return Response(data, status=200)

            if serializer.is_valid():
                data = serializer.data["token"]
                logger.info((f"✅ {data} < ----------- Новые данные"))
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
            )  # Используем logger.exception для трассировки
            return Response({"error": "Внутренняя ошибка сервера"}, status=500)


# class TestViewSet(APIView):
#     serializer_class = TestSerializer

#     def post(self, request):
#         return Response({"message": "Hello, world!"})
