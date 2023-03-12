from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.AllowedView)
admin.site.register(models.User)
