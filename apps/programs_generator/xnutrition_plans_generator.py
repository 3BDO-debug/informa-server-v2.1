from .utils import *
from .variables import nutrition_plan


def nutrition_plan_generator(
    generation_schema, meal_index, meal_food_items, required_macros, number_of_meals
):
    generated_plan = nutrition_plan

    for week_index in generated_plan:
        for day_index in generated_plan[week_index]:
            if generation_schema == "Balanced":
                generated_plan[week_index][day_index] = balanced(
                    meal_index, meal_food_items, required_macros, number_of_meals
                )
            elif generation_schema == "Refeed":
                pass
            
    return generated_plan


def balanced(meal_index, meal_food_items, required_macros, number_of_meals):

    meal_ratio = meals_ratios(number_of_meals).get(meal_index)

    food_items_data = [
        get_food_item_macros(food_item["id"]) for food_item in meal_food_items
    ]

    total_protein_per_meal = required_macros.get("protein_grams") * meal_ratio
    total_carbs_per_meal = required_macros.get("carb_grams") * meal_ratio
    total_fats_per_meal = required_macros.get("fat_grams") * meal_ratio

    main_protein_macros = total_protein_per_meal
    main_carbs_macros = total_carbs_per_meal * 0.90
    main_fats_macros = total_fats_per_meal * 0.90

    protein_food_items = get_meal_protein_food_items(food_items_data)
    carbs_food_items = get_meal_carbs_food_items(food_items_data)
    fats_food_items = get_meal_fats_food_items(food_items_data)

    """ Secondary meal items """

    secondary_protein_food_items = get_meal_secondary_protein_food_items(
        food_items_data
    )
    salad_food_items = get_meal_salad_food_items(food_items_data)
    fruits_food_items = get_meal_fruits_food_items(food_items_data)
    oil_food_items = get_meal_oil_food_items(food_items_data)

    """ Temporary computes """

    computed_protein = 0
    computed_carbs = 0
    computed_fats = 0

    """ Final result """

    result = []

    """ Mocking result """

    for food_item in food_items_data:
        result.append(
            {
                "id": food_item["id"],
                "name": food_item["name"],
                "serving": 0,
                "protein": 0,
                "carbs": 0,
                "fats": 0,
                "kcal": 0,
            }
        )

    """ Main protein items """

    if len(protein_food_items) > 0:
        while computed_protein < main_protein_macros:
            for protein_item in protein_food_items:

                macros = get_macros_per_serving(1, protein_item)

                computed_protein += macros["protein"]
                computed_carbs += macros["carbs"]
                computed_fats += macros["fats"]

                total_protein_per_meal -= macros["protein"]
                total_carbs_per_meal -= macros["carbs"]
                total_fats_per_meal -= macros["fats"]

                for index in range(len(result)):
                    if result[index]["name"] == protein_item["name"]:
                        item_to_be_updated = index

                result[item_to_be_updated]["serving"] += 1
                result[item_to_be_updated]["protein"] += macros["protein"]
                result[item_to_be_updated]["carbs"] += macros["carbs"]
                result[item_to_be_updated]["fats"] += macros["fats"]
                result[item_to_be_updated]["kcal"] += macros["kcal"]

    """ Main carbs items """

    if len(carbs_food_items) > 0:
        while computed_carbs < main_carbs_macros:
            for carb_item in carbs_food_items:

                macros = get_macros_per_serving(1, carb_item)

                computed_protein += macros["protein"]
                computed_carbs += macros["carbs"]
                computed_fats += macros["fats"]

                total_protein_per_meal -= macros["protein"]
                total_carbs_per_meal -= macros["carbs"]
                total_fats_per_meal -= macros["fats"]

                for index in range(len(result)):
                    if result[index]["name"] == carb_item["name"]:
                        item_to_be_updated = index

                result[item_to_be_updated]["serving"] += 1
                result[item_to_be_updated]["protein"] += macros["protein"]
                result[item_to_be_updated]["carbs"] += macros["carbs"]
                result[item_to_be_updated]["fats"] += macros["fats"]
                result[item_to_be_updated]["kcal"] += macros["kcal"]

    """ Main fats items """

    if len(fats_food_items) > 0:
        while computed_fats < main_fats_macros:
            for fat_item in fats_food_items:

                macros = get_macros_per_serving(1, fat_item)

                computed_protein += macros["protein"]
                computed_carbs += macros["carbs"]
                computed_fats += macros["fats"]

                total_protein_per_meal -= macros["protein"]
                total_carbs_per_meal -= macros["carbs"]
                total_fats_per_meal -= macros["fats"]

                for index in range(len(result)):
                    if result[index]["name"] == fat_item["name"]:
                        item_to_be_updated = index

                result[item_to_be_updated]["serving"] += 1
                result[item_to_be_updated]["protein"] += macros["protein"]
                result[item_to_be_updated]["carbs"] += macros["carbs"]
                result[item_to_be_updated]["fats"] += macros["fats"]
                result[item_to_be_updated]["kcal"] += macros["kcal"]

    """ Resetting computes """

    computed_protein = 0
    computed_carbs = 0
    computed_fats = 0

    """ Secondary protein items """

    if len(secondary_protein_food_items) > 0:
        while computed_protein < total_protein_per_meal:

            for secondary_protein_item in secondary_protein_food_items:

                macros = get_macros_per_serving(1, secondary_protein_item)

                computed_protein += macros["protein"]
                computed_carbs += macros["carbs"]
                computed_fats += macros["fats"]

                total_protein_per_meal -= macros["protein"]
                total_carbs_per_meal -= macros["carbs"]
                total_fats_per_meal -= macros["fats"]

                for index in range(len(result)):
                    if result[index]["name"] == secondary_protein_item["name"]:
                        item_to_be_updated = index

                result[item_to_be_updated]["serving"] += 1
                result[item_to_be_updated]["protein"] += macros["protein"]
                result[item_to_be_updated]["carbs"] += macros["carbs"]
                result[item_to_be_updated]["fats"] += macros["fats"]
                result[item_to_be_updated]["kcal"] += macros["kcal"]

    """ Salad items """

    if len(salad_food_items) > 0:
        while computed_carbs < total_carbs_per_meal:
            for salad_item in salad_food_items:

                macros = get_macros_per_serving(1, salad_item)

                computed_protein += macros["protein"]
                computed_carbs += macros["carbs"]
                computed_fats += macros["fats"]

                total_protein_per_meal -= macros["protein"]
                total_carbs_per_meal -= macros["carbs"]
                total_fats_per_meal -= macros["fats"]

                for index in range(len(result)):
                    if result[index]["name"] == salad_item["name"]:
                        item_to_be_updated = index

                result[item_to_be_updated]["serving"] += 1
                result[item_to_be_updated]["protein"] += macros["protein"]
                result[item_to_be_updated]["carbs"] += macros["carbs"]
                result[item_to_be_updated]["fats"] += macros["fats"]
                result[item_to_be_updated]["kcal"] += macros["kcal"]

    """ Fruits items """

    if len(fruits_food_items) > 0:
        while computed_carbs < total_carbs_per_meal:
            for fruit_item in fruits_food_items:

                macros = get_macros_per_serving(1, fruit_item)

                computed_protein += macros["protein"]
                computed_carbs += macros["carbs"]
                computed_fats += macros["fats"]

                total_protein_per_meal -= macros["protein"]
                total_carbs_per_meal -= macros["carbs"]
                total_fats_per_meal -= macros["fats"]

                for index in range(len(result)):
                    if result[index]["name"] == fruit_item["name"]:
                        item_to_be_updated = index

                result[item_to_be_updated]["serving"] += 1
                result[item_to_be_updated]["protein"] += macros["protein"]
                result[item_to_be_updated]["carbs"] += macros["carbs"]
                result[item_to_be_updated]["fats"] += macros["fats"]
                result[item_to_be_updated]["kcal"] += macros["kcal"]

    """ Oil items """

    if len(oil_food_items) > 0:
        while computed_fats < total_fats_per_meal:
            for oil_item in oil_food_items:

                macros = get_macros_per_serving(1, oil_item)

                computed_protein += macros["protein"]
                computed_carbs += macros["carbs"]
                computed_fats += macros["fats"]

                total_protein_per_meal -= macros["protein"]
                total_carbs_per_meal -= macros["carbs"]
                total_fats_per_meal -= macros["fats"]

                for index in range(len(result)):
                    if result[index]["name"] == oil_item["name"]:
                        item_to_be_updated = index

                result[item_to_be_updated]["serving"] += 1
                result[item_to_be_updated]["protein"] += macros["protein"]
                result[item_to_be_updated]["carbs"] += macros["carbs"]
                result[item_to_be_updated]["fats"] += macros["fats"]
                result[item_to_be_updated]["kcal"] += macros["kcal"]

    return result
