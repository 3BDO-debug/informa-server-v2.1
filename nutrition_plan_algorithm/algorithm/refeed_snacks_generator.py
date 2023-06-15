from meals.models import MealItem, Meal
from ..utils import (
    find_meal_items_by_category,
    get_food_item_macros,
    get_macros_per_serving,
)


def update_meal_item_data(data, meal_item, unit_macros):
    food_item_id = meal_item.food_item.id
    for index, item in enumerate(data):
        if item["food_item_id"] == food_item_id:
            data[index]["serving"] += 1
            data[index]["protein"] += unit_macros["protein"]
            data[index]["carbs"] += unit_macros["carbs"]
            data[index]["fats"] += unit_macros["fats"]
            data[index]["total_kcal"] += unit_macros["total_kcal"]
            break


def compute_carb_grams(items, target, data):
    computed_carb_grams = 0
    while computed_carb_grams < target:
        for meal_item in items:
            food_item_macros = get_food_item_macros(
                meal_item.food_item.id, meal_item.category
            )
            unit_macros = get_macros_per_serving(10, food_item_macros, False, None)
            computed_carb_grams += unit_macros["carbs"]
            update_meal_item_data(data, meal_item, unit_macros)
    return computed_carb_grams


def refeed_snacks_macros_generator(carbs_grams, snack_id):
    meal = Meal.objects.get(id=int(snack_id))
    meal_items = MealItem.objects.filter(meal=meal)

    main_carb_items = find_meal_items_by_category("Carb", meal_items)
    fruit_items = find_meal_items_by_category("Fruit", meal_items)
    salad_items = find_meal_items_by_category("Salad", meal_items)

    target_carb_grams = carbs_grams * 0.70
    target_secondary_carb = carbs_grams * (
        0.15 if len(fruit_items) > 0 and len(salad_items) > 0 else 0.30
    )

    data = [
        {
            "id": meal_item.id,
            "food_item_id": meal_item.food_item.id,
            "food_item_name": meal_item.food_item.en_name,
            "serving": 0
            if meal_item.category in ["Carb", "Fruit", "Salad"]
            else meal_item.serving,
            "protein": 0
            if meal_item.category in ["Carb", "Fruit", "Salad"]
            else meal_item.protein,
            "carbs": 0
            if meal_item.category in ["Carb", "Fruit", "Salad"]
            else meal_item.carbs,
            "fats": 0
            if meal_item.category in ["Carb", "Fruit", "Salad"]
            else meal_item.fats,
            "total_kcal": 0
            if meal_item.category in ["Carb", "Fruit", "Salad"]
            else meal_item.total_kcal,
        }
        for meal_item in meal_items
    ]

    compute_carb_grams(main_carb_items, target_carb_grams, data)

    for category_items in [fruit_items, salad_items]:
        if len(category_items) > 0:
            compute_carb_grams(category_items, target_secondary_carb, data)

    return data
