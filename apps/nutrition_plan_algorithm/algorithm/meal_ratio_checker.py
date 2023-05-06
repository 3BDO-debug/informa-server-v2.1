def meal_ratio_is_valid(*args, **kwargs):
    macros_per_meal = kwargs["macros_per_meal"]
    protein_per_meal = macros_per_meal["protein_per_meal"]
    carbs_per_meal = macros_per_meal["carbs_per_meal"]
    fats_per_meal = macros_per_meal["fats_per_meal"]

    computed_fats_via_ratio = (0.28 * protein_per_meal) + (0.06 * carbs_per_meal)

    meal_is_valid = True

    if computed_fats_via_ratio > fats_per_meal + 6:
        meal_is_valid = False

    return meal_is_valid
