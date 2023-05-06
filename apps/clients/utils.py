from .variables import *


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
