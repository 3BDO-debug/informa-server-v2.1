from .utils import *


def generate_meal_macros(meal_index, meal_food_items, required_macros, number_of_meals):

    print("Loading......")

    meal_ratio = meals_ratios(number_of_meals).get(meal_index)

    food_items_data = [
        get_food_item_macros(food_item["id"]) for food_item in meal_food_items
    ]

    protein_food_items = get_meal_protein_food_items(food_items_data)
    secondary_protein_food_items = get_meal_secondary_protein_food_items(
        food_items_data
    )
    carbs_food_items = get_meal_carbs_food_items(food_items_data)
    salad_food_items = get_meal_salad_food_items(food_items_data)
    fruits_food_items = get_meal_fruits_food_items(food_items_data)
    fats_food_items = get_meal_fats_food_items(food_items_data)
    oil_food_items = get_meal_oil_food_items(food_items_data)

    calories_per_meal = required_macros.get("total_calories") * meal_ratio

    total_protein_per_meal = required_macros.get("protein_grams") * meal_ratio
    total_carbs_per_meal = required_macros.get("carb_grams") * meal_ratio
    total_fats_per_meal = required_macros.get("fat_grams") * meal_ratio

    """ Distrbution of proteins among meal """

    protein_per_meal = 0.80 * total_protein_per_meal
    secondary_protein_per_meal = 0.10 * total_protein_per_meal

    """ Distrbution of carbs among meal """
    carbs_per_meal = 0.80 * total_carbs_per_meal
    salad_per_meal = 0.20 * total_carbs_per_meal
    fruits_per_meal = 0.20 * total_carbs_per_meal

    """ Distrbution of fats among meal  """
    fats_per_meal = 0.80 * total_fats_per_meal
    oil_per_meal = 0.20 * total_fats_per_meal

    computed_calories = 0
    computed_protein = 0
    computed_secondary_protein = 0
    computed_carbs = 0
    computed_salad = 0
    computed_fruits = 0
    computed_fats = 0
    computed_oil = 0

    result = []

    item_to_be_updated = 0

    """ Mocking result """
    for food_item in food_items_data:
        result.append(
            {
                "name": food_item["name"],
                "serving": 0,
            }
        )

    """ Adjust protein intake """

    if len(protein_food_items) > 0:
        while computed_protein < protein_per_meal:
            for protein_item in protein_food_items:
                computed_protein += get_macros_per_serving(1, protein_item)["protein"]

                for index in range(len(result)):
                    if result[index]["name"] == protein_item["name"]:
                        item_to_be_updated = index

                result[item_to_be_updated]["serving"] += 1

    """ Adjust secondary protein intake """

    if len(secondary_protein_food_items) > 0:
        while computed_secondary_protein < secondary_protein_per_meal:
            for secondary_protein_item in secondary_protein_food_items:
                computed_secondary_protein += get_macros_per_serving(
                    1, secondary_protein_item
                )["protein"]

                for index in range(len(result)):
                    if result[index]["name"] == secondary_protein_item["name"]:
                        item_to_be_updated = index

                result[item_to_be_updated]["serving"] += 1

    """ Adjust carbs intake """

    if len(carbs_food_items) > 0:
        while computed_carbs < carbs_per_meal:
            for carb_item in carbs_food_items:
                computed_carbs += get_macros_per_serving(1, carb_item)["carbs"]

                for index in range(len(result)):
                    if result[index]["name"] == carb_item["name"]:
                        item_to_be_updated = index

                result[item_to_be_updated]["serving"] += 1

    """ Adjust salad intake """

    if len(salad_food_items) > 0:
        while computed_salad < salad_per_meal:
            for salad_item in salad_food_items:
                computed_salad += get_macros_per_serving(1, salad_item)["carbs"]

                for index in range(len(result)):
                    if result[index]["name"] == salad_item["name"]:
                        item_to_be_updated = index

                result[item_to_be_updated]["serving"] += 1

    """ Adjust fruits intake """

    if len(fruits_food_items) > 0:
        while computed_fruits < fruits_per_meal:
            for fruit_item in fruits_food_items:
                computed_fruits += get_macros_per_serving(1, fruit_item)["carbs"]

                for index in range(len(result)):
                    if result[index]["name"] == fruit_item["name"]:
                        item_to_be_updated = index

                result[item_to_be_updated]["serving"] += 1

    """ Adjust fats intake """
    if len(fats_food_items) > 0:
        print("triggered")

        while computed_fats < fats_per_meal:
            for fat_item in fats_food_items:
                computed_fats += get_macros_per_serving(1, fat_item)["fats"]

                for index in range(len(result)):
                    if result[index]["name"] == fat_item["name"]:
                        item_to_be_updated = index

                result[item_to_be_updated]["serving"] += 1

    """ Adjust oil intake """

    if len(oil_food_items) > 0:
        while computed_oil < oil_per_meal:
            for oil_item in oil_food_items:
                computed_oil += get_macros_per_serving(1, oil_item)["fats"]

                for index in range(len(result)):
                    if result[index]["name"] == oil_item["name"]:
                        item_to_be_updated = index

                result[item_to_be_updated]["serving"] += 1

    print(f"Meal : {meal_index}", result)
