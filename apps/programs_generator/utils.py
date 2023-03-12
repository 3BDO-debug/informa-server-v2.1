from meals.models import FoodItem, Meal
from .variables import *
import json


def activity_level_value_calculator(user_training_volume, user_activity_per_day):

    fetched_user_training_volume_value = 1.2
    fetched_user_activity_per_day_value = 0

    total_activity_level_value = 1.2

    for training_volume in training_volume_data:
        if training_volume["label"] == user_training_volume:
            fetched_user_training_volume_value = training_volume["value"]

    for activity_per_day in activity_per_day_data:
        if activity_per_day["label"] == user_activity_per_day:
            fetched_user_activity_per_day_value = activity_per_day["value"]

    if fetched_user_training_volume_value + fetched_user_activity_per_day_value < 1.2:
        total_activity_level_value = 1.2
    else:
        total_activity_level_value = (
            fetched_user_training_volume_value + fetched_user_activity_per_day_value
        )

    return total_activity_level_value


def total_calories_calculator(user_weight, user_body_fat, activity_level_value):
    lean_body_mass = user_weight * (1 - (user_body_fat / 100))
    bmr = (lean_body_mass * 21.6) + 370

    total_calories = bmr * activity_level_value

    return {
        "lean_body_mass": lean_body_mass,
        "bmr": bmr,
        "total_calories": total_calories,
    }


def deficit_calories_calculator(total_calories, user_goal, user_body_fat):

    deficit = 0
    total_deficit_calories = 0

    for goal in goals_data:
        if goal["label"] == user_goal:
            if user_body_fat < 10:
                deficit = total_calories * goal["conditions"]["first_condition"]
            elif user_body_fat >= 10 and user_body_fat <= 15:
                deficit = total_calories * goal["conditions"]["second_condition"]
            elif user_body_fat > 15 and user_body_fat <= 20:
                deficit = total_calories * goal["conditions"]["third_condition"]
            elif user_body_fat > 20 and user_body_fat <= 25:
                deficit = total_calories * goal["conditions"]["fourth_condition"]
            elif user_body_fat > 25:
                deficit = total_calories * goal["conditions"]["fifth_condition"]

    if user_goal in negative_deficit:
        total_deficit_calories = total_calories - deficit
    else:
        total_deficit_calories = total_calories + deficit

    return int(total_deficit_calories)


def protein_macros_calculator(user_lean_body_mass, user_goal, user_body_fat):

    protein_grams = 0

    for protein_factor in protein_factor_data:
        if protein_factor["label"] == user_goal:
            if user_body_fat < 10:
                protein_grams = (
                    user_lean_body_mass
                    * 2.2
                    * protein_factor["conditions"]["first_condition"]
                )
            elif user_body_fat >= 10 and user_body_fat <= 15:
                protein_grams = (
                    user_lean_body_mass
                    * 2.2
                    * protein_factor["conditions"]["second_condition"]
                )
            elif user_body_fat > 15 and user_body_fat <= 20:
                protein_grams = (
                    user_lean_body_mass
                    * 2.2
                    * protein_factor["conditions"]["third_condition"]
                )
            elif user_body_fat > 20 and user_body_fat <= 25:
                protein_grams = (
                    user_lean_body_mass
                    * 2.2
                    * protein_factor["conditions"]["fourth_condition"]
                )
            elif user_body_fat > 25:
                protein_grams = (
                    user_lean_body_mass
                    * 2.2
                    * protein_factor["conditions"]["fifth_condition"]
                )

    return int(protein_grams)


def fat_macros_calculator(user_calories_deficit, user_goal):

    fat_grams = 0

    for fat_factor in fat_factor_data:
        if fat_factor["label"] == user_goal:
            fat_grams = (user_calories_deficit * fat_factor["value"]) / 9

    return int(fat_grams)


def carb_macros_calculator(user_calories_deficit, protein_macros, fat_macros):
    carb_grams = (user_calories_deficit - ((protein_macros * 4) + (fat_macros * 9))) / 4

    return int(carb_grams)


def meals_ratios(number_of_meals):

    meals_ratio = {}

    if number_of_meals == 2:
        meals_ratio.update({"meal_1": 0.65, "meal_2": 0.35})
    elif number_of_meals == 3:
        meals_ratio.update({"meal_1": 0.20, "meal_2": 0.50, "meal_3": 0.30})
    elif number_of_meals == 4:
        meals_ratio.update(
            {"meal_1": 0.20, "meal_2": 0.30, "meal_3": 0.30, "meal_4": 0.20}
        )

    return meals_ratio


def get_food_item_macros(food_item_id):
    food_item = FoodItem.objects.get(id=int(food_item_id))

    return {
        "id": food_item.id,
        "name": food_item.en_name,
        "category": food_item.category,
        "serving": food_item.serving,
        "protein": food_item.protein,
        "carbs": food_item.carbs,
        "fats": food_item.fats,
        "total_kcal": food_item.total_kcal,
    }


def get_macros_per_serving(serving, macros_data):
    unit_kcal = macros_data["total_kcal"] / macros_data["serving"]
    unit_protein = macros_data["protein"] / macros_data["serving"]
    unit_carb = macros_data["carbs"] / macros_data["serving"]
    unit_fat = macros_data["fats"] / macros_data["serving"]

    computed_calories = unit_kcal * serving
    computed_protein = unit_protein * serving
    computed_carbs = unit_carb * serving
    computed_fats = unit_fat * serving

    return {
        "kcal": computed_calories,
        "protein": computed_protein,
        "carbs": computed_carbs,
        "fats": computed_fats,
    }


def get_meal_protein_food_items(data):
    protein_items = []

    for item in data:
        if item["category"] == "Protein":
            protein_items.append(item)

    return protein_items


def get_meal_secondary_protein_food_items(data):
    secondary_protein_items = []

    for item in data:
        if item["category"] == "Secondary protein":
            secondary_protein_items.append(item)

    return secondary_protein_items


def get_meal_carbs_food_items(data):
    carbs_items = []

    for item in data:
        if item["category"] == "Carb":
            carbs_items.append(item)

    return carbs_items


def get_meal_salad_food_items(data):
    salad_food_items = []

    for item in data:
        if item["category"] == "Salad":
            salad_food_items.append(item)

    return salad_food_items


def get_meal_fruits_food_items(data):
    fruit_food_items = []

    for item in data:
        if item["category"] == "Fruit":
            fruit_food_items.append(item)

    return fruit_food_items


def get_meal_fats_food_items(data):
    fats_items = []

    for item in data:
        if item["category"] == "Fats":
            fats_items.append(item)

    return fats_items


def get_meal_oil_food_items(data):
    oil_food_items = []

    for item in data:
        if item["category"] == "Oil":
            oil_food_items.append(item)

    return oil_food_items


def filter_meals_by_index(index, data):

    result = []

    for meal in data:
        if index in [
            recommendation_index["id"]
            for recommendation_index in json.loads(meal.recommendation_indexes)
        ]:
            result.append(meal)

    return result


def snacks_recommendation_schema_matcher(schemas, required_macros):

    result = []

    for schema in schemas:
        if schema["range"]:
            if schema["start_range"] <= required_macros <= schema["end_range"]:
                for snack_name in schema["snacks"]:
                    snack = Meal.objects.get(name=snack_name)
                    result.append({"name": snack.name, "volume": 1, "id": snack.id})
        else:
            if required_macros > schema["start_range"]:
                for snack_name in schema["snacks"]:
                    snack = Meal.objects.get(name=snack_name)
                    result.append({"name": snack.name, "volume": 1, "id": snack.id})

    return result
