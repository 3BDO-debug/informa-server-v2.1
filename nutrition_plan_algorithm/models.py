from django.db import models
from clients.models import ClientData
from meals.models import Meal, FoodItem, MealItem


class NutritionPlan(models.Model):
    client_data = models.ForeignKey(
        ClientData, on_delete=models.CASCADE, verbose_name="Related client data"
    )
    schema = models.CharField(
        max_length=350, verbose_name="Nutrition plan generation schema"
    )
    is_active = models.BooleanField(default=False, verbose_name="Plan is active")
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name="Generated at")

    class Meta:
        verbose_name = "Nutrition plan"
        verbose_name_plural = "Nutrition plans"

    def __str__(self):
        return f"Nutrition plan for {self.client_data.client.user.first_name} {self.client_data.client.user.last_name} | {self.id} | {self.is_active}"


class NutritionPlanMeal(models.Model):
    nutrition_plan = models.ForeignKey(
        NutritionPlan, on_delete=models.CASCADE, verbose_name="Related nutrition plan"
    )
    meal = models.ForeignKey(
        Meal, on_delete=models.CASCADE, verbose_name="Related Meal"
    )
    meal_index = models.CharField(max_length=350, verbose_name="Meal index")
    meal_category = models.CharField(
        max_length=350, verbose_name="Meal Category"
    )  # is it refeed meal or main meal or refeed snack or main snack or low carb day meal or high carb day meal

    class Meta:
        verbose_name = "Nutrition plan meal"
        verbose_name_plural = "Nutrition plans meals"

    def __str__(self):
        return f"{self.nutrition_plan.id} | {self.meal.name} | {self.meal_index}"


class NutritionPlanMealItem(models.Model):
    nutrition_plan_meal = models.ForeignKey(
        NutritionPlanMeal,
        on_delete=models.CASCADE,
        verbose_name="Related nutrition plan meal",
    )
    meal_item = models.ForeignKey(
        MealItem, on_delete=models.CASCADE, verbose_name="Related meal item"
    )
    replaced = models.BooleanField(default=False, verbose_name="Replaced meal item")
    replaced_with = models.ForeignKey(
        FoodItem,
        on_delete=models.CASCADE,
        verbose_name="Replaced meal item with",
        related_name="replaced_meal_items",
        null=True,
        blank=True,
    )
    serving = models.IntegerField(verbose_name="Serving")
    protein = models.FloatField(verbose_name="Protein per serving", default=1.11)
    carbs = models.FloatField(verbose_name="Carbohydrates per serving", default=1.11)
    fats = models.FloatField(verbose_name="Fats per serving", default=1.11)
    total_kcal = models.FloatField(verbose_name="Total kcal", default=1.11)

    class Meta:
        verbose_name = "Nutrition plan meal item"
        verbose_name_plural = "Nutrition plans meal items"

    def __str__(self):
        return f"{self.nutrition_plan_meal.meal.name} -- {self.meal_item.food_item.en_name}"
