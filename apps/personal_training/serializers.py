from rest_framework.serializers import ModelSerializer
from . import models


class PersonalTrainingRequestSerializer(ModelSerializer):
    class Meta:
        model = models.PersonalTrainingRequest
        fields = "__all__"