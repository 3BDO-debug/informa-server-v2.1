from rest_framework.serializers import ModelSerializer
from . import models


class AnnouncementSerializer(ModelSerializer):
    class Meta:
        model = models.Announcement
        fields = "__all__"


class OfferItemSerializer(ModelSerializer):
    class Meta:
        model = models.OfferItem
        fields = "__all__"


class OfferSerializer(ModelSerializer):
    class Meta:
        model = models.Offer
        fields = "__all__"

    def to_representation(self, instance):
        data = super(OfferSerializer, self).to_representation(instance)
        offer_for = instance.offer_for.all()
        offer_for_serializer = OfferItemSerializer(offer_for, many=True)

        data["offer_for"] = offer_for_serializer.data

        return data
