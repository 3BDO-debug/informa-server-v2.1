from django.urls import path
from . import handlers


urlpatterns = [
    path("inject-db", handlers.inject_db),
    path("food-items-handler", handlers.FoodItemsHandler.as_view()),
    path("meals-types-handler", handlers.MealsTypesHandler.as_view()),
    path("meals-handler/<str:meal_type>", handlers.MealsHandler.as_view()),
    path("meal-details-handler/<int:meal_id>", handlers.MealDetailsHandler.as_view()),
    path("meal-items-handler/<int:meal_id>", handlers.MealItemsHandler.as_view()),
]
