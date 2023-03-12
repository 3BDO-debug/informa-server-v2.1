from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers


class SystemLogsHandler(APIView):
    def get(self, request):
        user = request.user

        if user.role == "manager" or user.is_superuser:
            system_logs = models.SystemLog.objects.all().order_by("-timestamp")
        else:
            system_logs = models.SystemLog.objects.filter(user=user).order_by(
                "-timestamp"
            )

        system_logs_serializer = serializers.SystemLogSerializer(system_logs, many=True)

        return Response(status=status.HTTP_200_OK, data=system_logs_serializer.data)

    def post(self, request):
        user = request.user
        action = request.data.get("action")

        models.SystemLog.objects.create(user=user, action=action).save()

        return Response(status=status.HTTP_200_OK)
