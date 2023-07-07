# Generated by Django 4.1.3 on 2023-01-09 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PersonalTrainingRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "fullname",
                    models.CharField(max_length=100, verbose_name="Full name"),
                ),
                (
                    "phone_number",
                    models.CharField(max_length=100, verbose_name="Phone Number"),
                ),
                (
                    "cor",
                    models.CharField(
                        max_length=100, verbose_name="Country of residence"
                    ),
                ),
                (
                    "paying_region",
                    models.CharField(max_length=100, verbose_name="Paying region"),
                ),
                ("age", models.IntegerField(verbose_name="Age")),
                ("gender", models.CharField(max_length=100, verbose_name="Gender")),
                ("weight", models.IntegerField(verbose_name="Weight")),
                ("height", models.FloatField(verbose_name="Height")),
                (
                    "plan_program",
                    models.CharField(max_length=100, verbose_name="Plan program"),
                ),
                (
                    "plan_duration",
                    models.CharField(max_length=100, verbose_name="Plan duration"),
                ),
                (
                    "followup_package",
                    models.CharField(max_length=100, verbose_name="Follow-up package"),
                ),
                (
                    "computed_total_price",
                    models.FloatField(verbose_name="Computed total price"),
                ),
                (
                    "computed_price_after_sale",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Computed price after sale"
                    ),
                ),
                (
                    "has_sale",
                    models.BooleanField(
                        default=False, verbose_name="Sale is activated"
                    ),
                ),
                (
                    "timestamp",
                    models.DateTimeField(auto_now_add=True, verbose_name="Timestamp"),
                ),
                (
                    "proceeded",
                    models.BooleanField(
                        default=False, verbose_name="Request is proceeded"
                    ),
                ),
            ],
            options={
                "verbose_name": "Personal training request",
                "verbose_name_plural": "Personal training requests",
            },
        ),
    ]