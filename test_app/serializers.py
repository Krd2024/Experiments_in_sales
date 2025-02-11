from rest_framework import serializers
from test_app.models import Device
from test_app.service.device_service import create_device, get_color_button


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["token"]

    def validate_token(self, token):
        # token = data.get("token")
        if Device.objects.filter(token=token).exists():
            # Вернуть объект с данными
            color_button = get_color_button(token)
            context = {"color_button": color_button}
            return context
        color_button = create_device(token)
        context = {"color_button": color_button}
        return context


# def update(self, instance, validated_data):
#     # Кастомная логика при обновлении
#     instance.token = validated_data.get("token", instance.token)
#     instance.save()
#     return instance
