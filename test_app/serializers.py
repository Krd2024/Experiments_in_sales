from rest_framework import serializers


class RequestSerializer(serializers.Serializer):
    DeviceToken = serializers.CharField(max_length=50, source="device-token")
