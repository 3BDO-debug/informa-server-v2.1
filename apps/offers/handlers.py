from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers


@api_view(["GET"])
def announcements_handler(request):
    active_announcement = models.Announcement.objects.filter(is_active=True)[0]
    active_announcement_serializer = serializers.AnnouncementSerializer(
        active_announcement, many=False
    )

    return Response(status=status.HTTP_200_OK, data=active_announcement_serializer.data)


@api_view(["GET"])
def offers_handler(request):
    offers = models.Offer.objects.all()[0]
    offers_serializer = serializers.OfferSerializer(offers, many=False)

    return Response(status=status.HTTP_200_OK, data=offers_serializer.data)
