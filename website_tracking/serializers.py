from rest_framework.serializers import ModelSerializer
from . import models


class WebsiteLogSerializer(ModelSerializer):
    class Meta:
        model = models.WebsiteLog
        fields = "__all__"
