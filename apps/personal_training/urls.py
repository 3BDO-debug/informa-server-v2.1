from django.urls import path
from . import handlers

urlpatterns = [
    path("request-personal-training", handlers.personal_training_requests_handler)
]
