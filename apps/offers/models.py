from django.db import models

# Create your models here.


class Announcement(models.Model):
    title = models.CharField(max_length=350, verbose_name="Announcement title")
    english_markdown = models.TextField(verbose_name="Announcement english markdown")
    arabic_markdown = models.TextField(verbose_name="Announcement arabic markdown")
    is_active = models.BooleanField(default=False, verbose_name="Activate announcement")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"

    def __str__(self):
        return self.title


class OfferItem(models.Model):
    name = models.CharField(max_length=350, verbose_name="Offer item value")

    def __str__(self):
        return self.name


class Offer(models.Model):
    title = models.CharField(max_length=350, verbose_name="Offer title")
    offer_for = models.ManyToManyField(OfferItem, verbose_name="Offer for")
    offer_percentage = models.IntegerField(verbose_name="Offer percentage")
    plan_duration_offer = models.BooleanField(
        default=False, verbose_name="Activate offer on plan duration"
    )
    plan_type_offer = models.BooleanField(
        default=False, verbose_name="Activate offer for plan type"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        verbose_name = "Offer"
        verbose_name_plural = "Offers"

    def __str__(self):
        return self.title
