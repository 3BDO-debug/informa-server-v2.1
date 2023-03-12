from django.urls import path
from . import handlers

urlpatterns = [
    path("request-personal-training", handlers.personal_training_requests_handler),
    path("personal-training-requests-data", handlers.personal_training_requests_data),
    path(
        "assign-personal-training-request-handler",
        handlers.assign_personal_training_request_handler,
    ),
    path(
        "proceed-personal-training-request", handlers.proceed_personal_training_request
    ),
]
