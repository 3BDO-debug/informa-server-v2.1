from rest_framework.serializers import ModelSerializer
from . import models


class InquirySerializer(ModelSerializer):
    class Meta:
        model = models.Inquiry
        fields = "__all__"
