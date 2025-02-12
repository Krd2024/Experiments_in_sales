from rest_framework import serializers
from loguru import logger


from test_app.service.device_service import cache_price, create_device
from test_app.models import Device


class RequestSerializer(serializers.Serializer):
    DeviceToken = serializers.CharField(max_length=50, source="device-token")


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["token"]

    def validate_token(self, token):
        print(token, "--- token in validate_token ---")
        try:
            if Device.objects.filter(token=token).exists():
                # Получить цвет кнопки и прайс
                data = cache_price(token)
                return data

            data = create_device(token)
            # context = {"color_button": color_button, "price": price}
            logger.info(data)
            return data
        except Exception as e:
            logger.error(f"Ошибка: {e}")


# def update(self, instance, validated_data):
#     # Кастомная логика при обновлении
#     instance.token = validated_data.get("token", instance.token)
#     instance.save()
#     return instance
