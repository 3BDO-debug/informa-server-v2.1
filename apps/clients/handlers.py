from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ast import literal_eval
from . import utils, models, serializers


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def clients_data_handler(request):

    subscription_id = request.data.get("id")
    fullname = request.data.get("fullName")
    weight = int(request.data.get("weight"))
    height = int(request.data.get("height"))
    age = int(request.data.get("age"))
    body_fat = int(request.data.get("fatPercentage"))
    body_fat_calc_method = request.data.get("bodyFatCalcMethod")
    training_volume = request.data.get("trainingVolume")
    activity_per_day = request.data.get("activityPerDay")
    goal = request.data.get("goal")
    excluded_food_items = literal_eval(request.data.get("excludedFoodItems"))
    can_take_protein_supplement = True

    number_of_meals = int(request.data.get("numberOfMeals"))

    activity_level_value = utils.activity_level_value_calculator(
        user_training_volume=training_volume, user_activity_per_day=activity_per_day
    )

    total_calories = utils.total_calories_calculator(
        user_weight=weight,
        user_body_fat=body_fat,
        activity_level_value=activity_level_value,
    )["total_calories"]

    bmr = utils.total_calories_calculator(
        user_weight=weight,
        user_body_fat=body_fat,
        activity_level_value=activity_level_value,
    )["bmr"]

    total_deficit_calories = utils.deficit_calories_calculator(
        total_calories=total_calories, user_goal=goal, user_body_fat=body_fat
    )

    lean_body_mass = utils.total_calories_calculator(
        user_weight=weight,
        user_body_fat=body_fat,
        activity_level_value=activity_level_value,
    )["lean_body_mass"]

    protein_grams = utils.protein_macros_calculator(
        user_lean_body_mass=lean_body_mass, user_goal=goal, user_body_fat=body_fat
    )

    fat_grams = utils.fat_macros_calculator(
        user_calories_deficit=total_deficit_calories, user_goal=goal
    )

    carb_grams = utils.carb_macros_calculator(
        user_calories_deficit=total_deficit_calories,
        protein_macros=protein_grams,
        fat_macros=fat_grams,
    )

    """ Creating client instance """

    client = models.Client.objects.get(subscription_id=subscription_id)

    """ Creating client data """
    client_data = models.ClientData.objects.filter(client=client)

    if len(client_data) > 0:
        """Find the client data that is set to active"""
        active_client_data = client_data.get(generate_using_this_data=True)
        active_client_data.generate_using_this_data = False
        active_client_data.save()

    client_data_obj = models.ClientData.objects.create(
        client=client,
        weight=weight,
        height=height,
        age=age,
        body_fat=body_fat,
        body_fat_calc_method=body_fat_calc_method,
        training_volume=training_volume,
        activity_per_day=activity_per_day,
        goal=goal,
        preferred_schema="Re-composition",
        can_take_protein_supplement=can_take_protein_supplement,
        number_of_meals=number_of_meals,
        lean_body_mass=lean_body_mass,
        bmr=bmr,
        total_calories=total_calories,
        calories_deficit=total_deficit_calories,
        protein_grams=protein_grams,
        fat_grams=fat_grams,
        carb_grams=carb_grams,
        generate_using_this_data=True,
    )

    if len(excluded_food_items) > 0:
        for food_item in excluded_food_items:

            client_data_obj.excluded_food_items.add(food_item)

    client.save()
    client_data_obj.save()

    return Response(status=status.HTTP_201_CREATED)


class ClientsDataHandler(APIView):
    def get(self, request, format=None):
        clients_data = models.Client.objects.all()
        clients_data_serializer = serializers.ClientSerializer(clients_data, many=True)

        return Response(data=clients_data_serializer.data, status=status.HTTP_200_OK)


class ClientDataHandler(APIView):
    def get(self, request, client_id, format=None):
        client_data = models.Client.objects.get(id=client_id)
        client_data_serializer = serializers.ClientSerializer(client_data, many=False)
        client_macros = models.ClientData.objects.filter(client=client_data).get(
            generate_using_this_data=True
        )
        client_macros_serializer = serializers.ClientDataSerializer(
            client_macros, many=False
        )

        return Response(
            data={
                "client_data": client_data_serializer.data,
                "client_computed_macros": client_macros_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
