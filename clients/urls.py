from django.urls import path
from . import handlers


urlpatterns = [
    path("client-data", handlers.clients_data_handler),
    path("clients-handler", handlers.ClientsDataHandler.as_view()),
    path("client-handler/<int:client_id>", handlers.ClientDataHandler.as_view()),
    path("client-macros-data-handler", handlers.ClientMacrosDataHandler.as_view()),
    path("generate-client-subscription-id", handlers.generate_client_subscription_id),
    path(
        "client-nutrition-plan-meals-handler",
        handlers.get_client_nutrition_plan_meals_handler,
    ),
    path("meals-in-take-tracking", handlers.MealInTakeTracking.as_view()),
    path("water-in-take-tracking", handlers.WaterInTakeTracking.as_view()),
    path("clients-follow-up-handler", handlers.ClientsFollowUpHandler.as_view()),
]
