from ..utils import meals_ratios


def optimize_macros(*args, **kwargs):
    required_macros = kwargs["required_macros"]
    number_of_meals = kwargs["number_of_meals"]
    meal_ratios = meals_ratios(number_of_meals)

    protein_per_day = required_macros["client_protein_grams"]
    carbs_per_day = required_macros["client_carb_grams"]
    fats_per_day = required_macros["client_fat_grams"]

    if number_of_meals == 3:
        # Check if meal 2 eligible for 28%-6%

        required_protien_per_meal = protein_per_day * meal_ratios["meal_2"]
        required_carbs_per_meal = carbs_per_day * meal_ratios["meal_2"]
        required_fats_per_meal = fats_per_day * meal_ratios["meal_2"]

        fats_per_protein_carbs = (0.28 * required_protien_per_meal) + (
            0.06 * required_carbs_per_meal
        )

        reduced_protein_grams = required_protien_per_meal

        while fats_per_protein_carbs > required_fats_per_meal:
            reduced_protein_grams -= 1

            fats_per_protein_carbs = (0.28 * reduced_protein_grams) + (
                0.06 * required_carbs_per_meal
            )

        excess_protein_grams = required_protien_per_meal - reduced_protein_grams


        return {
            "protein_per_meal": reduced_protein_grams,
            "carbs_per_meal": required_carbs_per_meal,
            "fats_per_meal": required_fats_per_meal,
            "excess_protein_grams": excess_protein_grams,
        }
