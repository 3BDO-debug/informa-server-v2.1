nutrition_plan = {
    "meals": None,
    "refeed_meals": None,
    "low_carb_days_meals": None,
    "high_carb_days_meals": None,
    "snacks": None,
    "refeed_snacks": None,
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
