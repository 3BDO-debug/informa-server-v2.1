from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers


@api_view(["GET"])
def website_logs_data(request):
    website_logs = models.WebsiteLog.objects.all().order_by("-timestamp")
    website_logs_serializer = serializers.WebsiteLogSerializer(website_logs, many=True)

    return Response(status=status.HTTP_200_OK, data=website_logs_serializer.data)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def website_logs_handler(request):
    action = request.data.get("action")
    platform = request.data.get("platform")
    user_device = request.data.get("userDevice")
    geo_location = request.data.get("region")

    models.WebsiteLog.objects.create(
        action=action,
        platform=platform,
        user_device=user_device,
        geo_location=geo_location,
    ).save()

    return Response(status=status.HTTP_200_OK)
