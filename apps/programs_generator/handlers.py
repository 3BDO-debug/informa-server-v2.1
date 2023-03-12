import json
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ast import literal_eval
from . import models, serializers, utils
from meals.models import Meal, MealItem
from meals.utils import meal_macros_generator
from meals.serializers import MealSerializer
from .meals_generator_v2 import generate_meal_macros
from .nutrition_plans_generator.main import nutrition_plan_generator
from .nutrition_plans_generator.balanced import balanced
from .variables import (
    protein_snacks_whey_included_recommendation_schema,
    protein_snacks_no_whey_recommendation_schema,
    carb_snacks_no_mass_gainer_recommendation_schema,
)
from .nutrition_plans_generator.psmf_generator import *


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def user_data_handler(request):

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
    prefered_food_items = literal_eval(request.data.get("preferedFoodItems"))
    can_take_protein_supplement = (
        True if request.data.get("canTakeProteinSupplement") == "yes" else False
    )

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

    """ Adding to the DB """

    client_data_obj = models.ClientData.objects.create(
        subscription_id=subscription_id,
        fullname=fullname,
        weight=weight,
        height=height,
        age=age,
        body_fat=body_fat,
        body_fat_calc_method=body_fat_calc_method,
        training_volume=training_volume,
        activity_per_day=activity_per_day,
        goal=goal,
        can_take_protein_supplement=can_take_protein_supplement,
        number_of_meals=number_of_meals,
    )

    if len(excluded_food_items) > 0:
        for food_item in excluded_food_items:

            client_data_obj.excluded_food_items.add(food_item)
    if len(prefered_food_items) > 0:
        for food_item in prefered_food_items:
            client_data_obj.prefered_food_items.add(food_item)

    """ Creating a db obj of user calculated macros """
    models.ClientMacros.objects.create(
        client=client_data_obj,
        lean_body_mass=lean_body_mass,
        bmr=bmr,
        total_calories=total_calories,
        calories_deficit=total_deficit_calories,
        protein_grams=protein_grams,
        fat_grams=fat_grams,
        carb_grams=carb_grams,
    ).save()

    client_data_obj.save()

    return Response(status=status.HTTP_201_CREATED)


class ClientsDataHandler(APIView):
    def get(self, request, format=None):
        clients_data = models.ClientData.objects.all().order_by("-timestamp")
        clients_data_serializer = serializers.ClientDataSerializer(
            clients_data, many=True
        )

        return Response(data=clients_data_serializer.data, status=status.HTTP_200_OK)


class ClientDataHandler(APIView):
    def get(self, request, client_id, format=None):
        client_data = models.ClientData.objects.get(id=client_id)
        client_data_serializer = serializers.ClientDataSerializer(
            client_data, many=False
        )
        client_macros = models.ClientMacros.objects.filter(
            client=client_data.id
        ).first()
        client_macros_serializer = serializers.ClientMacrosSerializer(
            client_macros, many=False
        )

        return Response(
            data={
                "client_data": client_data_serializer.data,
                "client_computed_macros": client_macros_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
def added_snacks_reciever(request):
    added_snacks = literal_eval(request.data.get("addedSnacks"))
    client_macros_data = literal_eval(request.data.get("clientMacrosData"))
    client_total_calories = client_macros_data.get("calories_deficit")
    client_protein_grams = client_macros_data.get("protein_grams")
    client_carb_grams = client_macros_data.get("carb_grams")
    client_fat_grams = client_macros_data.get("fat_grams")
    lean_body_mass = client_macros_data.get("lean_body_mass")

    for snack in added_snacks:
        snack_macros = meal_macros_generator(snack["id"])
        client_total_calories -= snack_macros["total_calories"] * float(snack["volume"])
        client_protein_grams -= snack_macros["total_protein_grams"] * float(
            snack["volume"]
        )
        client_carb_grams -= snack_macros["total_carbs_grams"] * float(snack["volume"])
        client_fat_grams -= snack_macros["total_fats_grams"] * float(snack["volume"])

    return Response(
        status=status.HTTP_200_OK,
        data={
            "client_total_calories": client_total_calories,
            "client_protein_grams": client_protein_grams,
            "client_carb_grams": client_carb_grams,
            "client_fat_grams": client_fat_grams,
            "lean_body_mass": lean_body_mass,
        },
    )


@api_view(["POST"])
def recommend_snacks_handler(request):
    client_data = json.loads(request.data.get("clientData"))
    required_macros = json.loads(request.data.get("clientMacros"))

    snacks = []

    """ Recommend protein snacks """

    protein_snacks_schema = (
        protein_snacks_whey_included_recommendation_schema
        if client_data["can_take_protein_supplement"]
        else protein_snacks_no_whey_recommendation_schema
    )

    carb_snacks_schema = carb_snacks_no_mass_gainer_recommendation_schema

    protein_snacks = utils.snacks_recommendation_schema_matcher(
        protein_snacks_schema, int(required_macros["protein_grams"])
    )

    """ Recommend carbs snacks """
    carb_snacks = utils.snacks_recommendation_schema_matcher(
        carb_snacks_schema, int(required_macros["carb_grams"])
    )

    """ Mocking results """

    for snack in protein_snacks:
        snacks.append(snack)

    for snack in carb_snacks:
        snacks.append(snack)

    return Response(status=status.HTTP_200_OK, data=snacks)


@api_view(["POST"])
def recommend_meal_presets(request):
    client_data = json.loads(request.data.get("clientData"))
    required_macros = json.loads(request.data.get("requiredMacros"))
    generation_schema = request.data.get("programSchema")

    meals = Meal.objects.filter(is_snack=False)

    plan_data = []

    for index in range(1, client_data["number_of_meals"] + 1):
        meal_index = f"meal_{index}"

        if index == 1:
            meals_data = MealSerializer(
                utils.filter_meals_by_index("breakfast", meals), many=True
            ).data
        elif index == 2:
            meals_data = MealSerializer(
                utils.filter_meals_by_index("lunch", meals), many=True
            ).data
        elif index == 3:
            index_value = "lunch" if client_data["number_of_meals"] > 3 else "dinner"
            meals_data = MealSerializer(
                utils.filter_meals_by_index(index_value, meals), many=True
            ).data
        else:
            meals_data = MealSerializer(
                utils.filter_meals_by_index("dinner", meals), many=True
            ).data

        for meal in meals_data:
            plan_data.append(
                {
                    "meal_id": meal["id"],
                    "meal_index": meal_index,
                    "name": meal["name"],
                    "food_items": balanced(
                        meal_index=meal_index,
                        meal_food_items=meal["food_items"],
                        required_macros={
                            "protein_grams": required_macros["client_protein_grams"],
                            "carb_grams": required_macros["client_carb_grams"],
                            "fat_grams": required_macros["client_fat_grams"],
                        },
                        number_of_meals=client_data["number_of_meals"],
                    ),
                }
            )

    return Response(status=status.HTTP_200_OK, data=plan_data)


@api_view(["POST"])
def generate_preset_macros(request):
    client_data = json.loads(request.data.get("clientData"))
    required_macros = json.loads(request.data.get("requiredMacros"))
    meal_preset_data = json.loads(request.data.get("mealPresetData"))
    meal_index = request.data.get("mealIndex")

    result = {
        "meal_id": meal_preset_data["id"],
        "meal_index": meal_index,
        "name": meal_preset_data["name"],
        "food_items": balanced(
            meal_index=meal_index,
            meal_food_items=meal_preset_data["food_items"],
            required_macros={
                "protein_grams": required_macros["client_protein_grams"],
                "carb_grams": required_macros["client_carb_grams"],
                "fat_grams": required_macros["client_fat_grams"],
            },
            number_of_meals=client_data["number_of_meals"],
        ),
    }

    return Response(status=status.HTTP_200_OK, data=result)


class GeneratePlans(APIView):
    def post(self, request, format=None):

        snacks_data = literal_eval(request.data.get("snacks"))
        meals_data = json.loads(request.data.get("mealsPresets"))
        number_of_meals = int(request.data.get("numberOfMeals"))
        client_macros_data = literal_eval(request.data.get("clientMacrosData"))
        program_schema = request.data.get("programSchema")

        client_total_calories = client_macros_data.get("calories_deficit")
        client_protein_grams = client_macros_data.get("protein_grams")
        client_carb_grams = client_macros_data.get("carb_grams")
        client_fat_grams = client_macros_data.get("fat_grams")

        nutrition_plan_snacks = []

        for snack in snacks_data:
            snack_macros = meal_macros_generator(snack["id"])
            client_total_calories -= snack_macros["total_calories"] * float(
                snack["volume"]
            )
            client_protein_grams -= snack_macros["total_protein_grams"] * float(
                snack["volume"]
            )
            client_carb_grams -= snack_macros["total_carbs_grams"] * float(
                snack["volume"]
            )
            client_fat_grams -= snack_macros["total_fats_grams"] * float(
                snack["volume"]
            )

            nutrition_plan_snacks.append(
                {
                    "snack_id": snack_macros["meal_id"],
                    "snack_name": snack_macros["meal_name"],
                    "volume": snack["volume"],
                    "total_calories": snack_macros["total_calories"]
                    * float(snack["volume"]),
                    "total_protein_grams": snack_macros["total_protein_grams"]
                    * float(snack["volume"]),
                    "total_carbs_grams": snack_macros["total_carbs_grams"]
                    * float(snack["volume"]),
                    "total_fats_grams": snack_macros["total_fats_grams"]
                    * float(snack["volume"]),
                }
            )

        """ Calling main algorithm driver """

        nutrition_plan = nutrition_plan_generator(
            meals_data=meals_data,
            generation_schema=program_schema,
            required_macros={
                "total_calories": client_total_calories,
                "deficit": int(client_macros_data.get("total_calories"))
                - int(client_macros_data.get("calories_deficit")),
                "protein_grams": client_protein_grams,
                "carb_grams": client_carb_grams,
                "fat_grams": client_fat_grams,
                "weight": client_macros_data["weight"],
            },
            number_of_meals=number_of_meals,
            refeed_snacks=json.loads(request.data.get("refeedSnacks"))
            if program_schema == "Refeed"
            else None,
        )
        return Response(
            status=status.HTTP_200_OK,
            data={"meals": nutrition_plan, "snacks": nutrition_plan_snacks},
        )


@api_view(["POST"])
def psmf_macros_handler(request):
    client_data = json.loads(request.data.get("clientData"))
    required_macros = json.loads(request.data.get("requiredMacros"))

    data = psmf_macros_generator(
        lean_body_mass=required_macros["lean_body_mass"],
        body_fat=client_data["body_fat"],
        number_of_meals=client_data["number_of_meals"],
        client_weight=client_data["weight"],
    )

    return Response(status=status.HTTP_200_OK, data=data)
