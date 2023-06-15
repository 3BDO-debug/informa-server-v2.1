from rest_framework.serializers import ModelSerializer
from . import models


class OnlineTrainingTaskSerializer(ModelSerializer):
    class Meta:
        model = models.OnlineTrainingTask
        fields = "__all__"

    def to_representation(self, instance):
        data = super(OnlineTrainingTaskSerializer, self).to_representation(instance)
        return data


class OnlineTrainingTaskMemberSerializer(ModelSerializer):
    class Meta:
        model = models.OnlineTrainingTaskMember
        fields = "__all__"
