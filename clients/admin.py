from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Client)
admin.site.register(models.ClientData)
admin.site.register(models.MealIntake)
admin.site.register(models.ClientFollowUp)
