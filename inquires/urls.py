from django.urls import path
from . import handlers

urlpatterns = [path("request-inquiry", handlers.inquires_handler)]
