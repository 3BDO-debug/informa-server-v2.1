training_volume_data = [
    {"label": "0-days", "value": 1.2},
    {"label": "1-2-days", "value": 1.25},
    {"label": "3-days", "value": 1.3},
    {"label": "4-days", "value": 1.4},
    {"label": "5-days", "value": 1.5},
    {"label": "6-days", "value": 1.6},
]


activity_per_day_data = [
    {"label": "sedentary", "value": -0.05},
    {"label": "light", "value": -0.025},
    {"label": "moderate", "value": 0},
    {"label": "active", "value": 0.025},
    {"label": "very-active", "value": 0.05},
]


goals_data = [
    {
        "label": "extreme-fat-loss",
        "conditions": {
            "first_condition": 0.375,
            "second_condition": 0.4,
            "third_condition": 0.4,
            "fourth_condition": 0.425,
            "fifth_condition": 0.45,
        },
    },
    {
        "label": "fat-loss",
        "conditions": {
            "first_condition": 0.275,
            "second_condition": 0.3,
            "third_condition": 0.3,
            "fourth_condition": 0.35,
            "fifth_condition": 0.375,
        },
    },
    {
        "label": "re-composition",
        "conditions": {
            "first_condition": 0.05,
            "second_condition": 0.1,
            "third_condition": 0.15,
            "fourth_condition": 0.2,
            "fifth_condition": 0.25,
        },
    },
    {
        "label": "clean-bulking",
        "conditions": {
            "first_condition": 0.3,
            "second_condition": 0.275,
            "third_condition": 0.275,
            "fourth_condition": 0.25,
            "fifth_condition": 0.225,
        },
    },
    {
        "label": "bulking",
        "conditions": {
            "first_condition": 0.45,
            "second_condition": 0.425,
            "third_condition": 0.425,
            "fourth_condition": 0.4,
            "fifth_condition": 0.375,
        },
    },
]


negative_deficit = ["extreme-fat-loss", "fat-loss", "re-composition"]


protein_factor_data = [
    {
        "label": "extreme-fat-loss",
        "conditions": {
            "first_condition": 1.35,
            "second_condition": 1.3,
            "third_condition": 1.3,
            "fourth_condition": 1.25,
            "fifth_condition": 1.2,
        },
    },
    {
        "label": "fat-loss",
        "conditions": {
            "first_condition": 1.4,
            "second_condition": 1.35,
            "third_condition": 1.3,
            "fourth_condition": 1.25,
            "fifth_condition": 1.2,
        },
    },
    {
        "label": "re-composition",
        "conditions": {
            "first_condition": 1.6,
            "second_condition": 1.55,
            "third_condition": 1.5,
            "fourth_condition": 1.45,
            "fifth_condition": 1.4,
        },
    },
    {
        "label": "clean-bulking",
        "conditions": {
            "first_condition": 1.6,
            "second_condition": 1.55,
            "third_condition": 1.5,
            "fourth_condition": 1.45,
            "fifth_condition": 1.4,
        },
    },
    {
        "label": "bulking",
        "conditions": {
            "first_condition": 1.6,
            "second_condition": 1.55,
            "third_condition": 1.5,
            "fourth_condition": 1.45,
            "fifth_condition": 1.4,
        },
    },
]


fat_factor_data = [
    {"label": "extreme-fat-loss", "value": 0.225},
    {"label": "fat-loss", "value": 0.25},
    {"label": "re-composition", "value": 0.25},
    {"label": "clean-bulking", "value": 0.3},
    {"label": "bulking", "value": 0.35},
]


nutrition_plan = {
    "week_1": {
        "day_1": None,
        "day_2": None,
        "day_3": None,
        "day_4": None,
        "day_5": None,
        "day_6": None,
        "day_7": None,
    },
    "week_2": {
        "day_1": None,
        "day_2": None,
        "day_3": None,
        "day_4": None,
        "day_5": None,
        "day_6": None,
        "day_7": None,
    },
    "week_3": {
        "day_1": None,
        "day_2": None,
        "day_3": None,
        "day_4": None,
        "day_5": None,
        "day_6": None,
        "day_7": None,
    },
    "week_4": {
        "day_1": None,
        "day_2": None,
        "day_3": None,
        "day_4": None,
        "day_5": None,
        "day_6": None,
        "day_7": None,
    },
}


carb_cycle_days_split = {
    "split_1": {
        "day_1": "low_carb",
        "day_2": "low_carb",
        "day_3": "low_carb",
        "day_4": "low_carb",
        "day_5": "high_carb",
        "day_6": "high_carb",
        "day_7": "high_carb",
    },
    "split_2": {
        "day_1": "low_carb",
        "day_2": "low_carb",
        "day_3": "low_carb",
        "day_4": "low_carb",
        "day_5": "low_carb",
        "day_6": "high_carb",
        "day_7": "high_carb",
    },
}


protein_snacks_whey_included_recommendation_schema = [
    {
        "range": True,
        "start_range": 150,
        "end_range": 185,
        "snacks": ["Molten Cake"],
    },
    {
        "range": True,
        "start_range": 185,
        "end_range": 200,
        "snacks": ["Whey Scoop", "Fruity Greek Yogurt"],
    },
    {
        "range": True,
        "start_range": 200,
        "end_range": 250,
        "snacks": ["Molten Cake", "Whey Scoop", "Fruity Greek Yogurt"],
    },
    {
        "range": False,
        "start_range": 250,
        "end_range": 250,
        "snacks": ["Molten Cake", "Whey Scoop", "Whey Scoop", "Fruity Greek Yogurt"],
    },
]


protein_snacks_no_whey_recommendation_schema = [
    {
        "range": True,
        "start_range": 185,
        "end_range": 210,
        "snacks": ["Fruity Greek Yogurt"],
    },
    {
        "range": False,
        "start_range": 210,
        "end_range": 210,
        "snacks": ["Fruity Greek Yogurt", "Fruity Greek Yogurt"],
    },
]


carb_snacks_no_mass_gainer_recommendation_schema = [
    {
        "range": True,
        "start_range": 150,
        "end_range": 180,
        "snacks": ["Fruit (25 gm)"],
    },
    {
        "range": True,
        "start_range": 180,
        "end_range": 200,
        "snacks": ["Fruit ( 50 gm)"],
    },
    {
        "range": True,
        "start_range": 200,
        "end_range": 250,
        "snacks": ["Oat Meal"],
    },
    {
        "range": True,
        "start_range": 250,
        "end_range": 300,
        "snacks": ["Super Shake"],
    },
    {
        "range": True,
        "start_range": 300,
        "end_range": 350,
        "snacks": ["Oat Meal", "Fruit ( 50 gm)"],
    },
    {
        "range": True,
        "start_range": 350,
        "end_range": 400,
        "snacks": ["Super Shake", "Fruit ( 50 gm)"],
    },
    {
        "range": False,
        "start_range": 400,
        "end_range": 400,
        "snacks": ["Super Shake", "Oat Meal"],
    },
]
