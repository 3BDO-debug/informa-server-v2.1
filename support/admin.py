from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.BugReport)
admin.site.register(models.SupportConversation)
admin.site.register(models.SupportConversationMessage)
admin.site.register(models.SupportInquiry)
admin.site.register(models.SupportInquiryMessage)
