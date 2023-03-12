from . import models


def meal_macros_generator(meal_id):
    meal = models.Meal.objects.get(id=meal_id)
    meal_items = models.MealItem.objects.filter(meal=meal)

    total_protein_grams = 0
    total_carbs_grams = 0
    total_fats_grams = 0
    total_calories = 0

    for meal_item in meal_items:
        total_protein_grams += int(meal_item.protein)
        total_carbs_grams += int(meal_item.carbs)
        total_fats_grams += int(meal_item.fats)
        total_calories += int(meal_item.total_kcal)

    return {
        "meal_id": meal.id,
        "meal_name": meal.name,
        "total_calories": total_calories,
        "total_protein_grams": total_protein_grams,
        "total_carbs_grams": total_carbs_grams,
        "total_fats_grams": total_fats_grams,
    }
