from .main import generate_meal_plan


def psmf_macros_generator(*args, **kwargs):
    lean_body_mass = kwargs["lean_body_mass"]
    body_fat = int(kwargs["body_fat"])
    number_of_meals = int(kwargs["number_of_meals"])
    client_weight = int(kwargs["client_weight"])

    """ Macros calculations """

    protein_grams = 0

    if body_fat < 10:
        protein_grams = lean_body_mass * 2.2 * 1.5

    elif body_fat >= 10 and body_fat < 15:
        protein_grams = lean_body_mass * 2.2 * 1.4

    elif body_fat >= 15:
        protein_grams = lean_body_mass * 2.2 * 1.3

    fat_grams = protein_grams * 0.15
    carb_grams = (number_of_meals * 10) + 10
    total_calories = (protein_grams * 4) + (carb_grams * 4) + (fat_grams * 9)

    return {
        "protein_grams": protein_grams,
        "carb_grams": carb_grams,
        "fat_grams": fat_grams,
        "calories_deficit": total_calories,
        "client_weight": client_weight,
    }


def psmf_driver_function(*args, **kwargs):
    lean_body_mass = kwargs["lean_body_mass"]
    body_fat = int(kwargs["body_fat"])
    number_of_meals = int(kwargs["number_of_meals"])

    action = kwargs["action"]

    required_macros = psmf_macros_generator(
        lean_body_mass=lean_body_mass,
        body_fat=body_fat,
        number_of_meals=number_of_meals,
    )

    result = None

    if action == "generate_macros":
        result = required_macros
    elif action == "generate_recommendations":
        meal_food_items = kwargs["meal_food_items"]
        meal_index = kwargs["meal_index"]
        result = generate_meal_plan(
            meal_food_items=meal_food_items,
            required_macros=required_macros,
        )
    elif action == "generate_plan":
        pass

    return result
