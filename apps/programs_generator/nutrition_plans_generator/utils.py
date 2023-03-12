from meals.models import Meal, MealItem
from ..utils import get_food_item_macros, get_macros_per_serving


def find_meal_items_by_category(category, data):
    result = []

    for item in data:
        if item.food_item.category == category:
            result.append(item)

    return result


def refeed_snacks_macros_generator(carbs_grams, snack_id):

    print("Called")
    target_carb_grams = carbs_grams * 0.70

    computed_carb_grams = 0

    meal = Meal.objects.get(id=int(snack_id))
    meal_items = MealItem.objects.filter(meal=meal)

    main_carb_items = find_meal_items_by_category("Carb", meal_items)
    fruit_items = find_meal_items_by_category("Fruit", meal_items)
    salad_items = find_meal_items_by_category("Salad", meal_items)

    if len(fruit_items) > 0 and len(salad_items) > 0:
        target_secondary_carb = carbs_grams * 0.15
    else:
        target_secondary_carb = carbs_grams * 0.30

    data = []

    """ Mock data """

    for meal_item in meal_items:
        food_item_id = meal_item.food_item.id
        if meal_item.food_item.category in ["Carb", "Fruit", "Salad"]:
            data.append(
                {
                    "food_item_id": food_item_id,
                    "food_item_name": meal_item.food_item.en_name,
                    "serving": 0,
                    "protein": 0,
                    "carbs": 0,
                    "fats": 0,
                    "kcal": 0,
                }
            )
        else:
            data.append(
                {
                    "food_item_id": food_item_id,
                    "food_item_name": meal_item.food_item.en_name,
                    "serving": meal_item.serving,
                    "protein": meal_item.protein,
                    "carbs": meal_item.carbs,
                    "fats": meal_item.fats,
                    "kcal": meal_item.total_kcal,
                }
            )

    while computed_carb_grams < target_carb_grams:
        for meal_item in main_carb_items:
            food_item_id = meal_item.food_item.id
            food_item_macros = get_food_item_macros(food_item_id)
            unit_macros = get_macros_per_serving(1, food_item_macros)

            computed_carb_grams += unit_macros["carbs"]

            """ Find index """
            for index in range(len(data)):
                if data[index]["food_item_id"] == food_item_id:
                    item_to_be_updated = index

            data[item_to_be_updated]["serving"] += 1
            data[item_to_be_updated]["protein"] += unit_macros["protein"]
            data[item_to_be_updated]["carbs"] += unit_macros["carbs"]
            data[item_to_be_updated]["fats"] += unit_macros["fats"]
            data[item_to_be_updated]["kcal"] += unit_macros["kcal"]

    computed_carb_grams = 0

    if len(fruit_items) > 0:
        while computed_carb_grams < target_secondary_carb:
            for meal_item in fruit_items:
                food_item_id = meal_item.food_item.id
                food_item_macros = get_food_item_macros(food_item_id)
                unit_macros = get_macros_per_serving(1, food_item_macros)

                computed_carb_grams += unit_macros["carbs"]

                """ Find index """
                for index in range(len(data)):
                    if data[index]["food_item_id"] == food_item_id:
                        item_to_be_updated = index

                data[item_to_be_updated]["serving"] += 1
                data[item_to_be_updated]["protein"] += unit_macros["protein"]
                data[item_to_be_updated]["carbs"] += unit_macros["carbs"]
                data[item_to_be_updated]["fats"] += unit_macros["fats"]
                data[item_to_be_updated]["kcal"] += unit_macros["kcal"]

    computed_carb_grams = 0

    if len(salad_items) > 0:
        while computed_carb_grams < target_secondary_carb:
            for meal_item in salad_items:
                food_item_id = meal_item.food_item.id
                food_item_macros = get_food_item_macros(food_item_id)
                unit_macros = get_macros_per_serving(1, food_item_macros)

                computed_carb_grams += unit_macros["carbs"]

                """ Find index """
                for index in range(len(data)):
                    if data[index]["food_item_id"] == food_item_id:
                        item_to_be_updated = index

                data[item_to_be_updated]["serving"] += 1
                data[item_to_be_updated]["protein"] += unit_macros["protein"]
                data[item_to_be_updated]["carbs"] += unit_macros["carbs"]
                data[item_to_be_updated]["fats"] += unit_macros["fats"]
                data[item_to_be_updated]["kcal"] += unit_macros["kcal"]

    return data
