from rest_framework.serializers import ModelSerializer
from . import models


class ClientDataSerializer(ModelSerializer):
    class Meta:
        model = models.ClientData
        fields = "__all__"


class ClientMacrosSerializer(ModelSerializer):
    class Meta:
        model = models.ClientMacros
        fields = "__all__"
