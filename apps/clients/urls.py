from django.urls import path
from . import handlers


urlpatterns = [
    path("client-data", handlers.clients_data_handler),
    path("clients-handler", handlers.ClientsDataHandler.as_view()),
    path("client-handler/<int:client_id>", handlers.ClientDataHandler.as_view()),
]
