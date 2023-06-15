from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def announcements_handler(request):
    try:
        active_announcement = models.Announcement.objects.filter(is_active=True)[0]
        active_announcement_serializer = serializers.AnnouncementSerializer(
            active_announcement, many=False
        )
        return Response(
            status=status.HTTP_200_OK, data=active_announcement_serializer.data
        )

    except:
        pass

    return Response(
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def offers_handler(request):
    try:
        offers = models.Offer.objects.all()
        offers_serializer = serializers.OfferSerializer(offers, many=True)

        return Response(status=status.HTTP_200_OK, data=offers_serializer.data)

    except:
        pass

    return Response(
        status=status.HTTP_200_OK,
    )
