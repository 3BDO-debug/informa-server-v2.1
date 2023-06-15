import json
import io
import copy
from django.db import transaction
from concurrent.futures import ThreadPoolExecutor
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ast import literal_eval
from meals.models import Meal, MealItem
from meals.utils import meal_macros_generator
from meals.serializers import MealSerializer
from clients.models import ClientData
from .variables import (
    protein_snacks_whey_included_recommendation_schema,
    protein_snacks_no_whey_recommendation_schema,
    carb_snacks_no_mass_gainer_recommendation_schema,
    nutrition_plan,
)
from .algorithm.schemas import nutrition_plan_generator
from .algorithm.psmf_generator import *
from .algorithm.optimize_macros import optimize_macros
from .utils import meals_ratios
from .algorithm.main import generate_meal_plan
from . import utils, models, serializers


@api_view(["POST"])
def added_snacks_reciever(request):
    added_snacks = json.loads(request.data.get("addedSnacks"))
    client_macros_data = json.loads(request.data.get("clientMacrosData"))
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
            "number_of_meals": client_macros_data["number_of_meals"],
        },
    )


@api_view(["POST"])
def recommend_snacks_handler(request):
    client_data = json.loads(request.data.get("clientData"))

    snacks = []

    """ Recommend protein snacks """

    protein_snacks_schema = (
        protein_snacks_whey_included_recommendation_schema
        if client_data["can_take_protein_supplement"]
        else protein_snacks_no_whey_recommendation_schema
    )

    carb_snacks_schema = carb_snacks_no_mass_gainer_recommendation_schema

    protein_snacks = utils.snacks_recommendation_schema_matcher(
        protein_snacks_schema, int(client_data["protein_grams"])
    )

    """ Recommend carbs snacks """
    carb_snacks = utils.snacks_recommendation_schema_matcher(
        carb_snacks_schema, int(client_data["carb_grams"])
    )

    """ Mocking results """

    for snack in protein_snacks:
        snacks.append(snack)

    for snack in carb_snacks:
        snacks.append(snack)

    return Response(status=status.HTTP_200_OK, data=snacks)


@api_view(["POST"])
def recommend_meal_presets(request):
    required_macros = json.loads(request.data.get("requiredMacros"))
    generation_schema = request.data.get("programSchema")

    meals = Meal.objects.filter(is_snack=False)
    plan_data = []
    required_meal_macros = optimize_macros(
        required_macros=required_macros,
        number_of_meals=required_macros["number_of_meals"],
    )

    meal_index_mapping = {
        1: "breakfast",
        2: "lunch",
        3: "lunch" if required_macros["number_of_meals"] > 3 else "dinner",
        4: "dinner",
    }

    def process_meal(index):
        meal_index = f"meal_{index}"
        index_value = meal_index_mapping.get(index)

        meals_data = MealSerializer(
            utils.filter_meals_by_index(index_value, meals), many=True
        ).data

        meal_data = []
        for meal in meals_data:
            meal_ratio = meals_ratios(required_macros["number_of_meals"]).get(
                meal_index
            )

            if required_macros["number_of_meals"] == 3 and (
                meal_index == "meal_1" or meal_index == "meal_3"
            ):
                optimized_macros_per_meal = required_meal_macros
                protein_per_meal = (
                    required_macros["client_protein_grams"] * meal_ratio
                ) + (
                    (0.3 if meal_index == "meal_1" else 0.7)
                    * optimized_macros_per_meal["excess_protein_grams"]
                )
            else:
                protein_per_meal = required_macros["client_protein_grams"] * meal_ratio

            carbs_per_meal = required_macros["client_carb_grams"] * meal_ratio
            fats_per_meal = required_macros["client_fat_grams"] * meal_ratio

            macros_per_meal = {
                "protein_per_meal": protein_per_meal,
                "carbs_per_meal": carbs_per_meal,
                "fats_per_meal": fats_per_meal,
            }

            meal_data.append(
                {
                    "meal_id": meal["id"],
                    "meal_index": meal_index,
                    "name": meal["name"],
                    "food_items": generate_meal_plan(
                        meal["food_items"], macros_per_meal
                    ),
                    "meal_ratio_is_valid": False,
                }
            )
        return meal_data

    with ThreadPoolExecutor() as executor:
        plan_data = list(
            executor.map(process_meal, range(1, required_macros["number_of_meals"] + 1))
        )

    plan_data = [meal for sublist in plan_data for meal in sublist]

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
        "food_items": generate_meal_plan(
            meal_food_items=meal_preset_data["food_items"],
            required_macros={
                "protein_grams": required_macros["client_protein_grams"],
                "carb_grams": required_macros["client_carb_grams"],
                "fat_grams": required_macros["client_fat_grams"],
            },
            number_of_meals=required_macros["number_of_meals"],
        ),
    }

    return Response(status=status.HTTP_200_OK, data=result)


class GeneratePlans(APIView):
    def process_snack(self, snack):
        snack_macros = meal_macros_generator(snack["id"])
        client_total_calories_delta = snack_macros["total_calories"] * float(
            snack["volume"]
        )
        client_protein_grams_delta = snack_macros["total_protein_grams"] * float(
            snack["volume"]
        )
        client_carb_grams_delta = snack_macros["total_carbs_grams"] * float(
            snack["volume"]
        )
        client_fat_grams_delta = snack_macros["total_fats_grams"] * float(
            snack["volume"]
        )

        return {
            "snack_id": snack_macros["meal_id"],
            "snack_name": snack_macros["meal_name"],
            "volume": snack["volume"],
            "total_calories": client_total_calories_delta,
            "total_protein_grams": client_protein_grams_delta,
            "total_carbs_grams": client_carb_grams_delta,
            "total_fats_grams": client_fat_grams_delta,
        }, (
            client_total_calories_delta,
            client_protein_grams_delta,
            client_carb_grams_delta,
            client_fat_grams_delta,
        )

    def post(self, request, format=None):
        snacks_data = literal_eval(request.data.get("snacks"))
        meals_data = json.loads(request.data.get("mealsPresets"))
        client_macros_data = json.loads(request.data.get("clientMacrosData"))
        number_of_meals = client_macros_data["number_of_meals"]

        program_schema = request.data.get("programSchema")

        client_total_calories = client_macros_data.get("calories_deficit")
        client_protein_grams = client_macros_data.get("protein_grams")
        client_carb_grams = client_macros_data.get("carb_grams")
        client_fat_grams = client_macros_data.get("fat_grams")

        nutrition_plan_snacks = []

        with ThreadPoolExecutor() as executor:
            snack_results = executor.map(self.process_snack, snacks_data)

        for snack_data, (
            calories_delta,
            protein_delta,
            carb_delta,
            fat_delta,
        ) in snack_results:
            client_total_calories -= calories_delta
            client_protein_grams -= protein_delta
            client_carb_grams -= carb_delta
            client_fat_grams -= fat_delta

            nutrition_plan_snacks.append(snack_data)

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
            snacks=nutrition_plan_snacks,
            refeed_snacks=json.loads(request.data.get("refeedSnacks"))
            if program_schema == "Refeed"
            else None,
        )

        return Response(
            status=status.HTTP_200_OK,
            data=nutrition_plan,
        )


class NutritionPlansHandler(APIView):
    def create_nutrition_plan_meal(self, data, meal_category, nutrition_plan_object):
        nutrition_plan_meals = []

        for meal in data:
            meal_obj, meal_index = self.get_meal_obj_and_index(meal, meal_category)

            nutrition_plan_meal_obj = models.NutritionPlanMeal(
                nutrition_plan=nutrition_plan_object,
                meal=meal_obj,
                meal_index=meal_index,
                meal_category=meal_category,
            )
            nutrition_plan_meals.append(nutrition_plan_meal_obj)

        created_nutrition_plan_meals = models.NutritionPlanMeal.objects.bulk_create(
            nutrition_plan_meals
        )

        nutrition_plan_meal_items = []
        for meal, created_nutrition_plan_meal in zip(
            data, created_nutrition_plan_meals
        ):
            meal_items = self.get_meal_items(
                meal, meal_category, created_nutrition_plan_meal.meal
            )

            for meal_item in meal_items:
                meal_item.nutrition_plan_meal = created_nutrition_plan_meal

            nutrition_plan_meal_items.extend(meal_items)

        models.NutritionPlanMealItem.objects.bulk_create(nutrition_plan_meal_items)

    def get_meal_obj_and_index(self, meal, meal_category):
        if meal_category == "snacks":
            preset_name = meal.get("snack_name")
            meal_index = "snack"
        elif meal_category == "refeed_snacks":
            preset_name = meal.get("preset_name")
            meal_index = "refeed_snack"
        else:
            preset_name = meal.get("preset_name")
            meal_index = meal.get("meal_index")

        meal_obj = Meal.objects.get(name=preset_name)

        return meal_obj, meal_index

    def get_meal_items(self, meal, meal_category, meal_obj):
        if meal_category == "snacks":
            meal_food_items = MealItem.objects.filter(meal=meal_obj)
        else:
            meal_food_items = meal.get("food_items")

        meal_items = []
        for meal_item in meal_food_items:
            if meal_category == "snacks":
                meal_item_obj = meal_item
                serving = meal_item.serving
                protein = meal_item.protein
                carbs = meal_item.carbs
                fats = meal_item.fats
                total_kcal = meal_item.total_kcal

            else:
                meal_item_obj = MealItem.objects.get(id=int(meal_item.get("id")))
                serving = meal_item.get("serving")
                protein = meal_item.get("protein")
                carbs = meal_item.get("carbs")
                fats = meal_item.get("fats")
                total_kcal = meal_item.get("total_kcal")

            meal_item_instance = models.NutritionPlanMealItem(
                meal_item=meal_item_obj,
                serving=serving,
                protein=protein,
                carbs=carbs,
                fats=fats,
                total_kcal=total_kcal,
            )
            meal_items.append(meal_item_instance)

        return meal_items

    def post(self, request):
        client_data_id = int(request.data.get("clientData")["id"])
        client_data = ClientData.objects.select_related("client").get(id=client_data_id)
        schema = request.data.get("schema")
        generated_nutrition_plan = request.data.get("generatedPlan")

        with transaction.atomic():
            models.NutritionPlan.objects.filter(
                client_data__client=client_data.client
            ).update(is_active=False)

            nutrition_plan = models.NutritionPlan.objects.create(
                client_data=client_data, schema=schema, is_active=True
            )

            meal_categories = [
                ("meals", "main_meals"),
                ("refeed_meals", "refeed_meals"),
                ("low_carb_days_meals", "low_carb_days_meals"),
                ("high_carb_days_meals", "high_carb_days_meals"),
                ("snacks", "snacks"),
                ("refeed_snacks", "refeed_snacks"),
            ]

            for category_key, category_name in meal_categories:
                meals = generated_nutrition_plan.get(category_key)
                if meals:
                    self.create_nutrition_plan_meal(
                        data=meals,
                        meal_category=category_name,
                        nutrition_plan_object=nutrition_plan,
                    )

            nutrition_plan.save()

        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        action = request.query_params.get("action")
        if action == "nutrition-plan-details":
            nutrition_plan_id = request.query_params.get("nutritionPlanId")
            nutrition_plan = models.NutritionPlan.objects.get(id=int(nutrition_plan_id))
            nutrition_plan_serializer = serializers.NutritionPlanSerializer(
                nutrition_plan, many=False
            )

            return Response(
                status=status.HTTP_200_OK, data=nutrition_plan_serializer.data
            )
        else:
            nutrition_plans = models.NutritionPlan.objects.all().order_by(
                "-generated_at"
            )
            nutrition_plans_serializer = serializers.NutritionPlanSerializer(
                nutrition_plans, many=True
            )

            return Response(
                status=status.HTTP_200_OK, data=nutrition_plans_serializer.data
            )


@api_view(["POST"])
def psmf_macros_handler(request):
    client_data = json.loads(request.data.get("clientData"))
    required_macros = json.loads(request.data.get("requiredMacros"))

    data = psmf_macros_generator(
        lean_body_mass=required_macros["lean_body_mass"],
        body_fat=required_macros["body_fat"],
        number_of_meals=required_macros["number_of_meals"],
        client_weight=required_macros["weight"],
    )

    return Response(status=status.HTTP_200_OK, data=data)


class NutritionPlanMealsHandler(APIView):
    def get(self, request):
        nutrition_plan_id = request.query_params.get("nutritionPlanId")
        nutrition_plan = models.NutritionPlan.objects.get(id=int(nutrition_plan_id))
        meal_category = request.query_params.get("mealCategory")
        nutrition_plan_meals = models.NutritionPlanMeal.objects.filter(
            nutrition_plan=nutrition_plan
        ).filter(meal_category=meal_category)
        nutrition_plan_meals_serializer = serializers.NutritionPlanMealSerializer(
            nutrition_plan_meals, many=True
        )

        return Response(
            status=status.HTTP_200_OK, data=nutrition_plan_meals_serializer.data
        )
