from django.contrib import admin
from import_export.admin import ExportActionMixin
from . import models


# Register your models here.


@admin.action(description="Mark selected as proceeded")
def make_proceeded(modeladmin, request, queryset):
    queryset.update(proceeded=True)


class PersonalTrainingRequestAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "pk",
        "fullname",
        "proceeded",
        "phone_number",
        "cor",
        "paying_region",
        "plan_program",
        "plan_duration",
        "followup_package",
        "computed_total_price",
        "timestamp",
    )

    actions = [make_proceeded]


admin.site.register(models.PersonalTrainingRequest, PersonalTrainingRequestAdmin)
