from rest_framework.serializers import ModelSerializer
from . import models


class SystemLogSerializer(ModelSerializer):
    class Meta:
        model = models.SystemLog
        fields = "__all__"

    def to_representation(self, instance):
        data = super(SystemLogSerializer, self).to_representation(instance)

        data["user_full_name"] = f"{instance.user.first_name} {instance.user.last_name}"

        return data
