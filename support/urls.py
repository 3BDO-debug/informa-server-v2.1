from django.urls import path
from . import handlers

urlpatterns = [
    path("bug-report", handlers.BugReportsHandler.as_view()),
    path("conversation-handler", handlers.ConversationHandler.as_view()),
    path("contacts-handler", handlers.contacts_handler),
    path(
        "conversation-messages-handler", handlers.ConversationMessagesHandler.as_view()
    ),
    path("support-inquires-handler", handlers.support_inquires_handler),
    path(
        "support-inquires-details-handler",
        handlers.SupportInquiryDetailsHandler.as_view(),
    ),
    path("check_inquires_limit", handlers.check_inquires_limit),
]
