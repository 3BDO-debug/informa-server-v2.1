from django.urls import path
from . import handlers

urlpatterns = [
    path("added-snacks-reciever", handlers.added_snacks_reciever),
    path("generate-plans", handlers.GeneratePlans.as_view()),
    path("recommend-snacks", handlers.recommend_snacks_handler),
    path("recomend-meals-presets", handlers.recommend_meal_presets),
    path("generate-preset-macros", handlers.generate_preset_macros),
    path("generate-psmf-macros", handlers.psmf_macros_handler),
]
