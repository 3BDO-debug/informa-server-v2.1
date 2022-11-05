from django.contrib import admin
from import_export.admin import ExportActionMixin
from . import models


# Register your models here.


class PersonalTrainingRequestAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "fullname",
        "phone_number",
        "cor",
        "payment_currency",
        "age",
        "gender",
        "weight",
        "height",
        "plan_program",
        "plan_duration",
        "followup_package",
        "computed_total_price",
        "timestamp",
    )


admin.site.register(models.PersonalTrainingRequest, PersonalTrainingRequestAdmin)
