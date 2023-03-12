from django.contrib import admin
from import_export.admin import ExportActionMixin
from . import models


# Register your models here.


class FoodItemAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "en_name",
        "ar_name",
        "protein",
        "fats",
        "carbs",
        "total_kcal",
        "created_at",
    )


admin.site.register(models.FoodItem, FoodItemAdmin)


admin.site.register(models.Meal)
admin.site.register(models.MealItem)
admin.site.register(models.MealType)
