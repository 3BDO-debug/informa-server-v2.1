from rest_framework.serializers import ModelSerializer
from . import models


class NutritionPlanSerializer(ModelSerializer):
    class Meta:
        model = models.NutritionPlan
        fields = "__all__"

    def to_representation(self, instance):
        data = super(NutritionPlanSerializer, self).to_representation(instance)
        data["client_goal"] = instance.client_data.goal

        return data


class NutritionPlanMealSerializer(ModelSerializer):
    class Meta:
        model = models.NutritionPlanMeal
        fields = "__all__"

    def find_meal_total_macros(self, food_items):
        data = {
            "total_protein": 0,
            "total_carbs": 0,
            "total_fats": 0,
            "total_calories": 0,
        }

        for food_item in food_items:
            data["total_protein"] += food_item.protein
            data["total_carbs"] += food_item.carbs
            data["total_fats"] += food_item.fats
            data["total_calories"] += food_item.total_kcal

        return data

    def to_representation(self, instance):
        data = super(NutritionPlanMealSerializer, self).to_representation(instance)
        data["meal_name"] = instance.meal.name
        food_items = models.NutritionPlanMealItem.objects.filter(
            nutrition_plan_meal=instance
        )
        data["food_items"] = NutritionPlanMealItemSerializer(
            food_items,
            many=True,
        ).data

        data["total_macros"] = self.find_meal_total_macros(food_items)

        return data


class NutritionPlanMealItemSerializer(ModelSerializer):
    class Meta:
        model = models.NutritionPlanMealItem
        fields = "__all__"

    def to_representation(self, instance):
        data = super(NutritionPlanMealItemSerializer, self).to_representation(instance)
        data["name"] = instance.meal_item.food_item.en_name

        return data
