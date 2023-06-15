from django.contrib import admin
from . import models

# Register your models here.


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")


admin.site.register(models.Announcement, AnnouncementAdmin)
admin.site.register(models.Offer)
admin.site.register(models.OfferItem)