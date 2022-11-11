from django.contrib import admin
from import_export.admin import ExportActionMixin
from . import models

# Register your models here.


class InquiryAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("id", "fullname", "proceeded", "phone_number", "email", "timestamp")


admin.site.register(models.Inquiry, InquiryAdmin)
