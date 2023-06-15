from django.urls import path
from . import handlers

urlpatterns = [
    path("website-logs-data", handlers.website_logs_data),
    path("website-logs-handler", handlers.website_logs_handler),
]
