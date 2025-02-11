from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from test_app.serializers import DeviceSerializer


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

    def post(self, request):
        device_token = request.headers.get("Device-Token")
        request.data["token"] = device_token
        serializer = self.get_serializer_class()(data=request.data)

        if serializer.is_valid():
            return Response(
                {"message": "POST request", "data": serializer.validated_data}
            )
        return Response(serializer.errors, status=400)


# class TestViewSet(APIView):
#     serializer_class = TestSerializer

#     def post(self, request):
#         return Response({"message": "Hello, world!"})
