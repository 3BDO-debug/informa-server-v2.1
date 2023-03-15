from django.db import models

# Create your models here.
class WebsiteLog(models.Model):
    action = models.CharField(max_length=350, verbose_name="Action")
    platform = models.CharField(max_length=350, verbose_name="Platform")
    user_device = models.CharField(max_length=350, verbose_name="User Device")
    geo_location = models.CharField(max_length=350, verbose_name="Geo Location")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")

    class Meta:
        verbose_name = "Website log"
        verbose_name_plural = "Website logs"

    def __str__(self):
        return f"New Log for {self.user_device} - {self.action}"
