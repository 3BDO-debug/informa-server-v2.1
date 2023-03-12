from django.db import models
from accounts.models import User

# Create your models here.


class PersonalTrainingRequest(models.Model):
    fullname = models.CharField(max_length=100, verbose_name="Full name")
    phone_number = models.CharField(max_length=100, verbose_name="Phone Number")
    cor = models.CharField(max_length=100, verbose_name="Country of residence")
    paying_region = models.CharField(max_length=100, verbose_name="Paying region")
    age = models.IntegerField(verbose_name="Age")
    gender = models.CharField(max_length=100, verbose_name="Gender")
    weight = models.IntegerField(verbose_name="Weight")
    height = models.FloatField(verbose_name="Height")
    plan_program = models.CharField(max_length=100, verbose_name="Plan program")
    plan_duration = models.CharField(max_length=100, verbose_name="Plan duration")
    followup_package = models.CharField(
        max_length=100, verbose_name="Follow-up package"
    )
    computed_total_price = models.FloatField(verbose_name="Computed total price")
    computed_price_after_sale = models.FloatField(
        verbose_name="Computed price after sale", null=True, blank=True
    )
    has_sale = models.BooleanField(default=False, verbose_name="Sale is activated")
    timestamp = models.DateTimeField(verbose_name="Timestamp")
    proceeded = models.BooleanField(default=False, verbose_name="Request is proceeded")
    proceeded_at = models.DateTimeField(verbose_name="Proceeded at", null=True)
    assigned_to = models.ForeignKey(
        User, verbose_name="Assigned To", on_delete=models.RESTRICT, null=True
    )

    class Meta:
        verbose_name = "Personal training request"
        verbose_name_plural = "Personal training requests"

    def __str__(self):
        return f"New request from {self.fullname}-{self.id}"
