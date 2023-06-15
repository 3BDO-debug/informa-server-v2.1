from rest_framework.serializers import ModelSerializer
from cloudinary import CloudinaryImage
from . import models
from clients.models import Client, ClientData
from nutrition_plan_algorithm.models import NutritionPlan


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

        if instance.profile_pic:
            data["profile_pic"] = CloudinaryImage(str(instance.profile_pic)).url

        if instance.role == "client":
            client = Client.objects.get(user=instance)
            client_data = ClientData.objects.filter(client=client).get(
                generate_using_this_data=True
            )
            active_nutrition_plan = NutritionPlan.objects.filter(
                client_data=client_data
            ).get(is_active=True)

            data["subscription_id"] = client.subscription_id
            data["follow_up_package"] = client.follow_up_package

            data["weight"] = client_data.weight
            data["body_fat"] = client_data.body_fat
            data["height"] = client_data.height
            data["number_of_meals"] = client_data.number_of_meals
            data["required_calories"] = client_data.calories_deficit
            data["water_in_take"] = client_data.water_in_take

            data["nutrition_plan_id"] = active_nutrition_plan.id
            data["nutrition_plan_schema"] = active_nutrition_plan.schema
            data["nutrition_plan_start_date"] = active_nutrition_plan.generated_at

        return data
