from django.contrib import admin
from . import models


# Register your models here.

admin.site.register(models.NutritionPlan)
admin.site.register(models.NutritionPlanMeal)
admin.site.register(models.NutritionPlanMealItem)
