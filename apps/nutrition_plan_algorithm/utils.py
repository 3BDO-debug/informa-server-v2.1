from meals.models import FoodItem, Meal
from .variables import *
import json


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


def get_food_item_macros(food_item_id, category):
    food_item = FoodItem.objects.get(id=int(food_item_id))

    return {
        "id": food_item.id,
        "category": category,
        "name": food_item.en_name,
        "serving": food_item.serving,
        "protein": food_item.protein,
        "carbs": food_item.carbs,
        "fats": food_item.fats,
        "total_kcal": food_item.total_kcal,
        "calc_per_piece": food_item.calc_per_piece,
        "per_piece_serving": food_item.per_piece_serving,
        "per_piece_name": food_item.per_piece_name,
    }


def get_macros_per_serving(serving, macros_data, get_data_by_id, food_item_id):

    if get_data_by_id:
        food_item = FoodItem.objects.get(id=int(food_item_id))
        macros_data = {
            "protein": food_item.protein,
            "carbs": food_item.carbs,
            "fats": food_item.fats,
            "total_kcal": food_item.total_kcal,
            "serving": food_item.serving,
        }

    unit_kcal = macros_data["total_kcal"] / macros_data["serving"]
    unit_protein = macros_data["protein"] / macros_data["serving"]
    unit_carb = macros_data["carbs"] / macros_data["serving"]
    unit_fat = macros_data["fats"] / macros_data["serving"]

    computed_calories = unit_kcal * serving
    computed_protein = unit_protein * serving
    computed_carbs = unit_carb * serving
    computed_fats = unit_fat * serving

    return {
        "serving": serving,
        "total_kcal": computed_calories,
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


def get_meal_food_item_by_category(data, category):
    result = []

    for item in data:
        if item["category"] == category:
            result.append(item)

    return result


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


def approx_to_closest_reference(ref_value, value):

    result = ref_value

    while result < value:
        measuring_index = result / 2
        if value > result + measuring_index:
            result += result
        else:
            break
    if result > value:
        if value > result / 2:
            pass
        else:
            result = 0

    return result


def find_meal_items_by_category(category, data):
    result = []
    for item in data:

        if item.category == category:
            result.append(item)

    return result


def mock_meals_presets(meals_presets):
    data = []

    for meal in meals_presets:
        for meal_preset in json.loads(meal["mealPresets"]):
            data.append(
                {
                    "meal_index": meal["mealIndex"],
                    "preset_name": meal_preset["name"],
                    "food_items": meal_preset["food_items"],
                }
            )

    return data


def get_servings(
    food_item,
    macros,
    total_items_per_category,
    secondary_items_exists,
):

    category = food_item["category"]
    unit_macros = get_macros_per_serving(1, None, True, food_item["food_item_id"])
    servings = 0

    protein_per_meal = macros["protein_per_meal"]
    carbs_per_meal = macros["carbs_per_meal"]
    fats_per_meal = macros["fats_per_meal"]

    if category == "Protein":
        if secondary_items_exists:
            servings = (
                (protein_per_meal * 0.85) / total_items_per_category
            ) / unit_macros["protein"]
        else:
            servings = (protein_per_meal / total_items_per_category) / unit_macros[
                "protein"
            ]

    elif category == "Secondary protein":
        servings = ((protein_per_meal * 0.15) / total_items_per_category) / unit_macros[
            "protein"
        ]

    elif category == "Carb":
        if secondary_items_exists:
            servings = (
                (carbs_per_meal * 0.83) / total_items_per_category
            ) / unit_macros["carbs"]
        else:
            servings = (carbs_per_meal / total_items_per_category) / unit_macros[
                "carbs"
            ]
    elif category == "Sauce":
        servings = ((carbs_per_meal * 0.17) / total_items_per_category) / unit_macros[
            "carbs"
        ]

    elif category == "Fats":
        if secondary_items_exists:
            servings = (
                (fats_per_meal * 0.80) / total_items_per_category
            ) / unit_macros["fats"]
        else:
            servings = fats_per_meal / total_items_per_category
    elif category == "Oil":
        servings = ((carbs_per_meal * 0.20) / total_items_per_category) / unit_macros[
            "fats"
        ]

    return servings


def get_items_by_category_macros(macro_category, food_items, value):
    data = []

    for food_item in food_items:
        unit_macros = get_macros_per_serving(1, None, True, food_item["food_item_id"])
        if unit_macros[macro_category] >= value:
            data.append(food_item)

    return data


def remove_excess_from_fats_items(data, excess):

    reduced_excess = excess
    excess_from_fats = 0

    main_fats_items = data["main_fats_items"]
    oil_items = data["oil_items"]

    food_items = []
    food_items.extend(main_fats_items)
    food_items.extend(oil_items)

    excess_from_fats = max(food_item["fats"])

    if len(main_fats_items) > 0 and len(oil_items) > 0:
        main_percentage = 0.80
        secondary_percentage = 0.20
    elif len(main_fats_items) > 0 and len(oil_items) == 0:
        main_percentage = 1
        secondary_percentage = 0
    elif len(oil_items) > 0 and len(main_fats_items) == 0:
        main_percentage = 0
        secondary_percentage = 1

    for food_item in food_items:
        unit_macros = get_macros_per_serving(1, None, True, food_item["food_item_id"])

        if food_item["category"] == "Fats":
            number_same_category_items = len(main_fats_items)
            excess_per_item = (main_percentage * excess) / number_same_category_items

            required_serving_per_item = excess_per_item / unit_macros["fats"]
        else:
            number_same_category_items = len(oil_items)
            excess_per_item = (
                secondary_percentage * excess
            ) / number_same_category_items

            required_serving_per_item = excess_per_item / unit_macros["fats"]

        macros_after_serving = get_macros_per_serving(
            required_serving_per_item, None, True, food_item["food_item_id"]
        )
        reduced_excess -= macros_after_serving["fats"]

    return reduced_excess
