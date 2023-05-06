from copy import deepcopy
from ..utils import *


def generate_meal_plan(meal_food_items, required_macros):
    meal_plan = initialize_meal_plan(meal_food_items)

    meal_plan = calculate_initial_servings(meal_plan, required_macros)

    meal_plan = adjust_servings(meal_plan, required_macros, total_kcal_tolerance=10)

    return meal_plan


def initialize_meal_plan(meal_food_items):
    meal_plan = []

    for food_item in meal_food_items:

        try:
            food_item_name = food_item["name"]
        except:
            food_item_name = food_item["food_item"]["en_name"]

        meal_plan.append(
            {
                "id": food_item["id"],
                "name": food_item_name,
                "food_item_id": food_item["food_item_id"],
                "category": food_item["category"],
                "serving": 0,
                "protein": 0,
                "carbs": 0,
                "fats": 0,
                "total_kcal": 0,
            }
        )

    return meal_plan


def calculate_initial_servings(meal_plan, required_macros):
    for food_item in meal_plan:

        items_per_food_item_category = len(
            get_meal_food_item_by_category(meal_plan, food_item["category"])
        )
        secondary_items_exists = False

        if food_item["category"] == "Protein":
            number_of_secondary_items = get_meal_food_item_by_category(
                meal_plan, "Secondary protein"
            )

            if len(number_of_secondary_items) > 0:
                secondary_items_exists = True
        elif food_item["category"] == "Carb":
            number_of_secondary_items = get_meal_food_item_by_category(
                meal_plan, "Sauce"
            )
            if len(number_of_secondary_items) > 0:
                secondary_items_exists = True
        elif food_item["category"] == "Fats":
            number_of_secondary_items = get_meal_food_item_by_category(meal_plan, "Oil")

            if len(number_of_secondary_items) > 0:
                secondary_items_exists = True

        servings_needed = get_servings(
            food_item,
            {
                "protein_per_meal": required_macros["protein_per_meal"],
                "carbs_per_meal": required_macros["carbs_per_meal"],
                "fats_per_meal": required_macros["fats_per_meal"],
            },
            items_per_food_item_category,
            secondary_items_exists,
        )

        macros_per_servings = get_macros_per_serving(
            servings_needed, None, True, food_item["food_item_id"]
        )

        food_item["serving"] = int(servings_needed)
        food_item["protein"] = macros_per_servings["protein"]
        food_item["carbs"] = macros_per_servings["carbs"]
        food_item["fats"] = macros_per_servings["fats"]
        food_item["total_kcal"] = macros_per_servings["total_kcal"]

    return meal_plan


def adjust_servings(meal_plan, required_macros, total_kcal_tolerance):
    protein_per_meal = required_macros.get("protein_per_meal")
    carbs_per_meal = required_macros.get("carbs_per_meal")
    fats_per_meal = required_macros.get("fats_per_meal")
    total_kcal_per_meal = (
        (protein_per_meal * 4) + (carbs_per_meal * 4) + (fats_per_meal * 9)
    )

    max_iterations = 1000
    iteration = 0
    alternate = True

    while iteration < max_iterations:
        prev_meal_plan = deepcopy(meal_plan)

        computed_macros = compute_macros(meal_plan)
        excess_in_kcal = computed_macros["total_kcal"] - total_kcal_per_meal

        if abs(excess_in_kcal) <= total_kcal_tolerance:
            break

        fats_reduced = False
        for food_item in meal_plan:
            unit_macros = get_macros_per_serving(
                1, None, True, food_item["food_item_id"]
            )

            if excess_in_kcal > total_kcal_tolerance and food_item["category"] in [
                "Fats",
                "Oil",
            ]:
                if food_item["serving"] > 0:
                    food_item["serving"] -= 1
                    food_item["fats"] -= unit_macros["fats"]
                    food_item["protein"] -= unit_macros["protein"]
                    food_item["carbs"] -= unit_macros["carbs"]

                    food_item["total_kcal"] -= unit_macros["total_kcal"]
                    excess_in_kcal -= unit_macros["total_kcal"]
                    fats_reduced = True

        if not fats_reduced:
            for food_item in meal_plan:
                unit_macros = get_macros_per_serving(
                    1, None, True, food_item["food_item_id"]
                )

                if alternate:
                    if excess_in_kcal > total_kcal_tolerance and food_item[
                        "category"
                    ] in ["Protein", "Secondary protein"]:
                        if food_item["serving"] > 0:
                            food_item["serving"] -= 1
                            food_item["fats"] -= unit_macros["fats"]
                            food_item["protein"] -= unit_macros["protein"]
                            food_item["carbs"] -= unit_macros["carbs"]

                            food_item["total_kcal"] -= unit_macros["total_kcal"]
                            excess_in_kcal -= unit_macros["total_kcal"]
                else:
                    if excess_in_kcal > total_kcal_tolerance and food_item[
                        "category"
                    ] in ["Carb"]:
                        if food_item["serving"] > 0:
                            food_item["serving"] -= 1
                            food_item["fats"] -= unit_macros["fats"]
                            food_item["protein"] -= unit_macros["protein"]
                            food_item["carbs"] -= unit_macros["carbs"]

                            food_item["total_kcal"] -= unit_macros["total_kcal"]
                            excess_in_kcal -= unit_macros["total_kcal"]

                alternate = not alternate

        iteration += 1

        if meal_plan == prev_meal_plan:
            break

    return meal_plan


def compute_macros(meal_plan):
    total_macros = {"protein": 0, "carbs": 0, "fats": 0, "total_kcal": 0}

    for food_item in meal_plan:
        total_macros["protein"] += food_item["protein"]
        total_macros["carbs"] += food_item["carbs"]
        total_macros["fats"] += food_item["fats"]
        total_macros["total_kcal"] += food_item["total_kcal"]

    return total_macros
