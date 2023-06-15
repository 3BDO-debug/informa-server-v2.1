from django.urls import path
from . import handlers


urlpatterns = [
    path("announcements-data", handlers.announcements_handler),
    path("offers-data", handlers.offers_handler),
]
