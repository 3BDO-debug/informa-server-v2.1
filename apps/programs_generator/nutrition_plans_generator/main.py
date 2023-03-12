import copy
import json
from ..variables import nutrition_plan, carb_cycle_days_split
from .balanced import balanced
from meals import models as meals_models
from meals.utils import meal_macros_generator
from .utils import refeed_snacks_macros_generator


def balanced_daily_meals_adder(*args, **kwargs):
    meals_data = kwargs["meals_data"]

    data = []
    for meal in meals_data:
        for meal_preset in json.loads(meal["mealPresets"]):
            data.append(
                {
                    "meal_index": meal["mealIndex"],
                    "preset_name": meal_preset["name"],
                    "food_items": balanced(
                        meal_index=meal["mealIndex"],
                        meal_food_items=meal_preset["food_items"],
                        required_macros=kwargs["macros"],
                        number_of_meals=kwargs["number_of_meals"],
                    ),
                }
            )
    return data


def refeed_daily_meals_adder(*args, **kwargs):
    macros = copy.deepcopy(kwargs["macros"])
    refeed_snacks = kwargs["refeed_snacks"]
    extra_carb_grams = macros["carb_grams"]

    refeed_snacks_data = []

    for snack in refeed_snacks:
        preset_content = []
        for snack_preset in snack["content"]:
            preset_content.append(
                {
                    "option_name": snack_preset["label"],
                    "food_items": refeed_snacks_macros_generator(
                        snack_id=snack_preset["id"],
                        carbs_grams=(macros["carb_grams"] * 0.60 / len(refeed_snacks)),
                    ),
                }
            )

        refeed_snacks_data.append(
            {"preset_id": snack["presetId"], "content": preset_content}
        )

    # macros_after_snacks

    macros["carb_grams"] = extra_carb_grams * 0.40

    generated_plan = balanced_daily_meals_adder(
        meals_data=kwargs["meals_data"],
        macros=macros,
        number_of_meals=kwargs["number_of_meals"],
    )

    result = {"refeed_snacks": refeed_snacks_data, "meals": generated_plan}

    return result


def carb_cycle_daily_meals_adder(*args, **kwargs):
    day_index = kwargs["day"]
    macros = kwargs["macros"]

    days_split = (
        carb_cycle_days_split["split_1"]
        if macros["carb_grams"] > 85
        else carb_cycle_days_split["split_2"]
    )

    number_of_low_carb_days = 4 if macros["carb_grams"] > 85 else 5
    number_of_high_carb_days = 3 if macros["carb_grams"] > 85 else 2

    low_carb_day_carbs_grams = (
        (macros["carb_grams"] * 7) * 0.40
    ) / number_of_low_carb_days
    high_carb_day_carbs_grams = (
        (macros["carb_grams"] * 7) * 0.60
    ) / number_of_high_carb_days

    new_macros = copy.deepcopy(macros)
    new_macros["carb_grams"] = (
        low_carb_day_carbs_grams
        if days_split[day_index] == "low_carb"
        else high_carb_day_carbs_grams
    )

    generate_plan = balanced_daily_meals_adder(
        meals_data=kwargs["meals_data"],
        macros=new_macros,
        number_of_meals=kwargs["number_of_meals"],
    )

    return generate_plan


def nutrition_plan_generator(*args, **kwargs):
    generated_plan = nutrition_plan

    meals_data = kwargs["meals_data"]
    generation_schema = kwargs["generation_schema"]
    required_macros = kwargs["required_macros"]
    number_of_meals = kwargs["number_of_meals"]

    # In case of refeed

    refeed_cases = {"week_1": ["day_7"], "week_3": ["day_6", "day_7"]}

    for week_index in generated_plan:
        for day_index in generated_plan[week_index]:
            if generation_schema == "Balanced":
                generated_plan[week_index][day_index] = balanced_daily_meals_adder(
                    meals_data=meals_data,
                    macros=required_macros,
                    number_of_meals=number_of_meals,
                )

            elif generation_schema == "Refeed":
                if week_index in refeed_cases:
                    if day_index in refeed_cases[week_index]:
                        extra_carbs = required_macros["deficit"] / 4
                        refeed_macros = copy.deepcopy(required_macros)
                        refeed_macros["carb_grams"] += extra_carbs

                        generated_plan[week_index][
                            day_index
                        ] = refeed_daily_meals_adder(
                            meals_data=meals_data,
                            macros=refeed_macros,
                            number_of_meals=number_of_meals,
                            refeed_snacks=kwargs["refeed_snacks"],
                        )
                    else:
                        generated_plan[week_index][
                            day_index
                        ] = balanced_daily_meals_adder(
                            meals_data=meals_data,
                            macros=required_macros,
                            number_of_meals=number_of_meals,
                        )
                else:
                    generated_plan[week_index][day_index] = balanced_daily_meals_adder(
                        meals_data=meals_data,
                        macros=required_macros,
                        number_of_meals=number_of_meals,
                    )

            elif generation_schema == "Carb cycle":
                generated_plan[week_index][day_index] = carb_cycle_daily_meals_adder(
                    day=day_index,
                    meals_data=meals_data,
                    macros=required_macros,
                    number_of_meals=number_of_meals,
                )
            elif generation_schema == "PSMF":

                if day_index == "day_7":

                    psmf_refeed = copy.deepcopy(required_macros)
                    psmf_refeed["carb_grams"] += required_macros["weight"] * 2
                    generated_plan[week_index][day_index] = balanced_daily_meals_adder(
                        meals_data=meals_data,
                        macros=psmf_refeed,
                        number_of_meals=number_of_meals,
                    )

                else:
                    generated_plan[week_index][day_index] = balanced_daily_meals_adder(
                        meals_data=meals_data,
                        macros=required_macros,
                        number_of_meals=number_of_meals,
                    )

    return generated_plan
