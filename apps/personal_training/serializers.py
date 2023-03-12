from rest_framework.serializers import ModelSerializer
from . import models


class PersonalTrainingRequestSerializer(ModelSerializer):
    class Meta:
        model = models.PersonalTrainingRequest
        fields = "__all__"

    def to_representation(self, instance):
        data = super(PersonalTrainingRequestSerializer, self).to_representation(
            instance
        )

        if instance.assigned_to:
            data[
                "assigned_to_name"
            ] = f"{instance.assigned_to.first_name} {instance.assigned_to.last_name}"
        else:
            data["assigned_to_name"] = "Not Assigned Yet"

        return data
