from rest_framework.serializers import ModelSerializer
from . import models
from accounts.serializers import UserSerializer


class ClientSerializer(ModelSerializer):
    class Meta:
        model = models.Client
        fields = "__all__"

    def to_representation(self, instance):
        data = super(ClientSerializer, self).to_representation(instance)
        data["fullname"] = f"{instance.user.first_name} {instance.user.last_name}"
        data["username"] = instance.user.username
        data["email"] = instance.user.email
        try:
            currently_active_client_data = models.ClientData.objects.filter(
                client=instance
            ).get(generate_using_this_data=True)
        except:
            currently_active_client_data = None
        data["body_fat"] = (
            currently_active_client_data.body_fat
            if currently_active_client_data
            else "Not yet available"
        )
        data["training_volume"] = (
            currently_active_client_data.training_volume
            if currently_active_client_data
            else "Not yet available"
        )
        data["activity_per_day"] = (
            currently_active_client_data.activity_per_day
            if currently_active_client_data
            else "Not yet available"
        )
        data["goal"] = (
            currently_active_client_data.goal
            if currently_active_client_data
            else "Not yet available"
        )

        return data


class ClientDataSerializer(ModelSerializer):
    class Meta:
        model = models.ClientData
        fields = "__all__"


class ClientFollowUpSerializer(ModelSerializer):
    class Meta:
        model = models.ClientFollowUp
        fields = "__all__"

    def to_representation(self, instance):
        data = super(ClientFollowUpSerializer, self).to_representation(instance)

        client = instance.client.user
        coach = instance.coach

        data["client_data"] = UserSerializer(client, many=False).data
        data["coach_data"] = UserSerializer(coach, many=False).data
        
        return data
