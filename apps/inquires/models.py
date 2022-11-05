from django.db import models

# Create your models here.


class Inquiry(models.Model):
    fullname = models.CharField(max_length=100, verbose_name="Full name")
    phone_number = models.CharField(max_length=100, verbose_name="Phone number")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Message")

    class Meta:
        verbose_name = "Inquiry"
        verbose_name_plural = "Inquiries"

    def __str__(self):
        return f"New inquiry from {self.fullname}-${self.id}"
