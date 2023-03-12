from rest_framework.serializers import ModelSerializer
from . import models


class FoodItemSerializer(ModelSerializer):
    class Meta:
        model = models.FoodItem
        fields = "__all__"


class MealTypeSerializer(ModelSerializer):
    class Meta:
        model = models.MealType
        fields = "__all__"


class MealSerializer(ModelSerializer):
    class Meta:
        model = models.Meal
        fields = "__all__"

    def to_representation(self, instance):
        data = super(MealSerializer, self).to_representation(instance)
        food_items = []
        meal_items = models.MealItem.objects.filter(meal=instance.id)
        for meal_item in meal_items:
            food_items.append(FoodItemSerializer(meal_item.food_item, many=False).data)
        data["food_items"] = food_items
        data["meal_type_name"] = instance.meal_type.name

        return data


class MealItemSerializer(ModelSerializer):
    class Meta:
        model = models.MealItem
        fields = "__all__"

    def to_representation(self, instance):
        data = super(MealItemSerializer, self).to_representation(instance)
        data["food_item_name"] = instance.food_item.en_name
        return data
