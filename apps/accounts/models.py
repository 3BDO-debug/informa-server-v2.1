from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


# Create your models here.


class AllowedView(models.Model):
    name = models.CharField(max_length=350, verbose_name="Allowed View Name")
    slug = models.SlugField(verbose_name="Allowed view slug", blank=True, null=True)
    description = models.TextField(verbose_name="Allowed View Description", null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Allowed View"
        verbose_name_plural = "Allowed Views"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(AllowedView, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class User(AbstractUser):
    role = models.CharField(max_length=350, verbose_name="Role", null=True)
    allowed_views = models.ManyToManyField(
        AllowedView, verbose_name="Allowed Views", null=True, blank=True
    )
    is_logged_in = models.BooleanField(
        default=False, verbose_name="This user is logged in"
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
