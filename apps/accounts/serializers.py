from rest_framework.serializers import ModelSerializer
from . import models


class AllowedViewSerializer(ModelSerializer):
    class Meta:
        model = models.AllowedView
        fields = "__all__"


class UserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        allowed_views = []

        for allowed_view in data["allowed_views"]:
            allowed_views.append(
                AllowedViewSerializer(
                    models.AllowedView.objects.get(id=allowed_view), many=False
                ).data
            )

        data["allowed_views_data"] = allowed_views

        return data
