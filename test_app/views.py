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
        request=DeviceSerializer,
    )
    def post(self, request):
        print("--- POST ---")
        try:
            device_token = request.headers.get("Device-Token")

            data = action_choice_token(device_token)
            logger.debug(data)
            if data:
                return Response(data, status=200)

            # Добавить токен
            request.data["token"] = device_token
            print(request.data, "--- request.data in POST---")

            serializer = self.get_serializer_class()(data=request.data)

            if serializer.is_valid():
                data = serializer.data["token"]
                logger.info(data)
                return Response({"data": data})

            logger.error(serializer.errors)
            return Response(serializer.errors, status=400)

        except IntegrityError:
            print("--- except IntegrityError ---")
            data = cache_price(device_token)
            logger.info(data)
            return Response(serializer.errors, status=400)
        except Exception as e:
            logger.error(f"Ошибка {e}")
            return Response(serializer.errors, status=400)


# class TestViewSet(APIView):
#     serializer_class = TestSerializer

#     def post(self, request):
#         return Response({"message": "Hello, world!"})
