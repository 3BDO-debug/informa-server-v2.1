from django.urls import path
from . import handlers

urlpatterns = [
    path("logout", handlers.logout_handler),
    path("allowed-views-handler", handlers.allowed_views_handler),
    path("accounts-handler", handlers.AccountHandler.as_view()),
    path("account-details", handlers.account_details_handler),
    path("active-users-data", handlers.active_users_data),
]
