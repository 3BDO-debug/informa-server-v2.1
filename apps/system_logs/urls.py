from django.urls import path
from . import handlers

urlpatterns = [path("system-logs-handler", handlers.SystemLogsHandler.as_view())]
