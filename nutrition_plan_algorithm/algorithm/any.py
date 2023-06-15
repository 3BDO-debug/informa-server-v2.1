import copy
import json
from ..variables import nutrition_plan, carb_cycle_days_split
from .main import generate_meal_plan
from .optimize_macros import optimize_macros
from ..utils import meals_ratios
from .refeed_snacks_generator import refeed_snacks_macros_generator
from ..utils import mock_meals_presets


class Schema:
    def __init__(
        self, meals_data, required_macros, number_of_meals, refeed_snacks=None
    ):
        self.meals_data = meals_data
        self.required_macros = required_macros
        self.number_of_meals = number_of_meals
        self.refeed_snacks = refeed_snacks

    def daily_meals(self, week_index, day_index):
        pass


class BalancedSchema(Schema):
    def daily_meals(self, week_index, day_index):
        return mock_meals_presets(self.meals_data)


class RefeedSchema(Schema):
    def daily_meals(self, week_index, day_index):
        refeed_cases = {"week_1": ["day_7"], "week_3": ["day_6", "day_7"]}

        is_refeed_day = (
            week_index in refeed_cases and day_index in refeed_cases[week_index]
        )

        if is_refeed_day:
            extra_carbs = self.required_macros["deficit"] / 4
            refeed_macros = copy.copy(self.required_macros)
            refeed_macros["carb_grams"] += extra_carbs
            return refeed_daily_meals_adder(
                self.meals_data, refeed_macros, self.number_of_meals, self.refeed_snacks
            )
        else:
            return mock_meals_presets(self.meals_data)


class CarbCycleSchema(Schema):
    def daily_meals(self, week_index, day_index):
        return carb_cycle_daily_meals_adder(
            day_index, self.meals_data, self.required_macros, self.number_of_meals
        )


class PSMFSchema(Schema):
    def daily_meals(self, week_index, day_index):
        if day_index == "day_7":
            psmf_refeed = copy.copy(self.required_macros)
            psmf_refeed["carb_grams"] += self.required_macros["weight"] * 2
            return balanced_daily_meals_adder(
                self.meals_data, psmf_refeed, self.number_of_meals
            )
        else:
            return mock_meals_presets(self.meals_data)


def create_schema_instance(
    generation_schema, meals_data, required_macros, number_of_meals, refeed_snacks=None
):
    if generation_schema == "Balanced":
        return BalancedSchema(
            meals_data, required_macros, number_of_meals, refeed_snacks
        )
    elif generation_schema == "Refeed":
        return RefeedSchema(meals_data, required_macros, number_of_meals, refeed_snacks)
    elif generation_schema == "Carb cycle":
        return CarbCycleSchema(
            meals_data, required_macros, number_of_meals, refeed_snacks
        )
    elif generation_schema == "PSMF":
        return PSMFSchema(meals_data, required_macros, number_of_meals, refeed_snacks)
    else:
        raise ValueError(f"Unknown generation_schema: {generation_schema}")


def nutrition_plan_generator(
    meals_data, generation_schema, required_macros, number_of_meals, refeed_snacks=None
):
    schema_instance = create_schema_instance(
        generation_schema, meals_data, required_macros, number_of_meals, refeed_snacks
    )
    generated_plan = copy.deepcopy(nutrition_plan)

    for week_index in generated_plan:
        for day_index in generated_plan[week_index]:
            daily_meals = schema_instance.daily_meals(week_index, day_index)
            generated_plan[week_index][day_index] = daily_meals

    return generated_plan


def balanced_daily_meals_adder(meals_data, macros, number_of_meals):
    data = []

    def calculate_macros_per_meal(
        meal_index, macros, meal_ratios, required_meal_macros
    ):
        meal_ratio = meal_ratios.get(meal_index)
        protein_per_meal = macros["protein_grams"] * meal_ratio
        carbs_per_meal = macros["carb_grams"] * meal_ratio
        fats_per_meal = macros["fat_grams"] * meal_ratio

        if number_of_meals == 3 and (meal_index == "meal_1" or meal_index == "meal_3"):
            optimized_macros_per_meal = required_meal_macros
            protein_per_meal += (
                0.3 if meal_index == "meal_1" else 0.7
            ) * optimized_macros_per_meal["excess_protein_grams"]

        return {
            "protein_per_meal": protein_per_meal,
            "carbs_per_meal": carbs_per_meal,
            "fats_per_meal": fats_per_meal,
        }

    required_macros = {
        "client_protein_grams": macros["protein_grams"],
        "client_carb_grams": macros["carb_grams"],
        "client_fat_grams": macros["fat_grams"],
    }
    required_meal_macros = optimize_macros(
        required_macros=required_macros, number_of_meals=number_of_meals
    )
    meal_ratios = meals_ratios(number_of_meals)

    for meal in meals_data:
        for meal_preset in json.loads(meal["mealPresets"]):
            meal_index = meal_preset["meal_index"]
            required_macros_per_meal = calculate_macros_per_meal(
                meal_index, macros, meal_ratios, required_meal_macros
            )

            data.append(
                {
                    "meal_index": meal["mealIndex"],
                    "preset_name": meal_preset["name"],
                    "food_items": generate_meal_plan(
                        meal_food_items=meal_preset["food_items"],
                        required_macros=required_macros_per_meal,
                    ),
                }
            )
    return data


def refeed_daily_meals_adder(meals_data, macros, number_of_meals, refeed_snacks):
    refeed_snacks_data = []
    macros["carb_grams"] = macros["carb_grams"] + (macros["deficit"] / 4)

    for snack in refeed_snacks:
        snack_data = {"preset_name": snack["presetId"], "food_items": None}

        for snack_preset in snack["content"]:
            food_item = refeed_snacks_macros_generator(
                snack_id=snack_preset["id"],
                carbs_grams=(macros["carb_grams"] * 0.60 / len(refeed_snacks)),
            )
            snack_data["preset_name"] = snack_preset["label"]
            snack_data["food_items"] = food_item

        refeed_snacks_data.append(snack_data)

    macros["carb_grams"] *= 0.40

    generated_plan = balanced_daily_meals_adder(meals_data, macros, number_of_meals)

    return {"refeed_snacks": refeed_snacks_data, "meals": generated_plan}


def carb_cycle_daily_meals_adder(day, meals_data, macros, number_of_meals):
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

    new_macros = copy.copy(macros)
    new_macros["carb_grams"] = (
        low_carb_day_carbs_grams
        if days_split[day] == "low_carb"
        else high_carb_day_carbs_grams
    )

    return balanced_daily_meals_adder(meals_data, new_macros, number_of_meals)