import numpy as np
import pandas as pd
import json
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from . import models, serializers


def inject_db(request):
    file = pd.read_excel("food_items.xlsx", sheet_name=0)
    rows = len(file)
    for row_index in range(rows):
        row_data = file.loc[row_index].values
        models.FoodItem.objects.create(
            category=row_data[0],
            en_name=row_data[1],
            serving=int(row_data[2]),
            protein=float(row_data[3]),
            carbs=float(row_data[4]),
            fats=float(row_data[5]),
            total_kcal=float(row_data[6]),
            ar_name=row_data[7],
        ).save()


class FoodItemsHandler(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        food_items = models.FoodItem.objects.all().order_by("-created_at")
        food_items_serializer = serializers.FoodItemSerializer(food_items, many=True)

        return Response(food_items_serializer.data, status=status.HTTP_200_OK)


class MealsTypesHandler(APIView):
    def get(self, request):
        meals_types = models.MealType.objects.all().order_by("-created_at")
        meals_types_serializer = serializers.MealTypeSerializer(meals_types, many=True)
        return Response(status=status.HTTP_200_OK, data=meals_types_serializer.data)

    def post(self, request):
        name = request.data.get("name")
        models.MealType.objects.create(name=name).save()
        return Response(status=status.HTTP_200_OK)


class MealsHandler(APIView):
    def get(self, request, meal_type, format=None):
        meals = models.Meal.objects.all().order_by("-created_at")
        meals_serializer = serializers.MealSerializer(meals, many=True)

        return Response(data=meals_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, meal_type, format=None):
        is_snack = True if meal_type == "snack" else False
        name = request.data.get("name")
        is_refeed_snack = request.data.get("isRefeedSnack")
        meal_category = models.MealType.objects.get(
            id=int(request.data.get("mealCategory"))
        )
        recommendation_months = json.dumps(request.data.get("recommendationMonths"))
        recommendation_indexes = json.dumps(request.data.get("recommendationIndexes"))

        meal_obj = models.Meal.objects.create(
            name=name,
            meal_type=meal_category,
            is_snack=is_snack,
            is_refeed_snack=is_refeed_snack,
            contain_protein_supplement=request.data.get("containProteinSupplement"),
            recommendation_months=recommendation_months,
            recommendation_indexes=recommendation_indexes,
        )
        meal_obj_serializer = serializers.MealSerializer(meal_obj, many=False)
        return Response(data=meal_obj_serializer.data, status=status.HTTP_201_CREATED)


class MealDetailsHandler(APIView):
    def get(self, request, meal_id, format=None):
        meal = models.Meal.objects.get(id=meal_id)
        meal_serializer = serializers.MealSerializer(meal, many=False)
        return Response(data=meal_serializer.data, status=status.HTTP_200_OK)


class MealItemsHandler(APIView):
    def get(self, request, meal_id, format=None):
        meal = models.Meal.objects.get(id=meal_id)
        meal_items = models.MealItem.objects.filter(meal=meal)
        meal_items_serializer = serializers.MealItemSerializer(meal_items, many=True)
        return Response(data=meal_items_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, meal_id, format=None):
        meal = models.Meal.objects.get(id=meal_id)
        food_item = models.FoodItem.objects.get(id=request.data.get("foodItem")["id"])
        serving = request.data.get("serving") if meal.is_snack else 1
        food_item_protein_per_gram = food_item.protein / food_item.serving
        protein_grams = food_item_protein_per_gram * serving
        food_item_carbs_per_gram = food_item.carbs / food_item.serving
        carbs_grams = food_item_carbs_per_gram * serving
        food_item_fats_per_gram = food_item.fats / food_item.serving
        fats_grams = food_item_fats_per_gram * serving
        food_item_kcal_per_gram = food_item.total_kcal / food_item.serving
        kcal = food_item_kcal_per_gram * serving

        models.MealItem.objects.create(
            meal=meal,
            food_item=food_item,
            serving=serving,
            protein=protein_grams,
            carbs=carbs_grams,
            fats=fats_grams,
            total_kcal=kcal,
        ).save()

        return Response(status=status.HTTP_200_OK)
