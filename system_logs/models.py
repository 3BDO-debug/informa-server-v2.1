from django.db import models
from accounts.models import User

# Create your models here.


class SystemLog(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.RESTRICT, verbose_name="Action Done By"
    )
    action = models.TextField(verbose_name="Action Description")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")

    class Meta:
        verbose_name = "System log"
        verbose_name_plural = "System logs"

    def __str__(self):
        return f"{self.user.first_name} - {self.action}"
