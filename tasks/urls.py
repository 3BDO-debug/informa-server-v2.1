from django.urls import path
from . import handlers


urlpatterns = [
    path("online-training-tasks-handler", handlers.OnlineTrainingTasksHandler.as_view())
]
