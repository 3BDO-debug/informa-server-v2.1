from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.MuscleGroup)

admin.site.register(models.Muscle)

admin.site.register(models.Equipment)
admin.site.register(models.Excercise)
admin.site.register(models.Injury)
