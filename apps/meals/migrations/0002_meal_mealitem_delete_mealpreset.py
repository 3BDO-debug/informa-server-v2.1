# Generated by Django 4.1.3 on 2023-01-09 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("meals", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Meal",
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
                ("name", models.CharField(max_length=350, verbose_name="Meal name")),
                (
                    "is_snack",
                    models.BooleanField(default=False, verbose_name="Is snack ?"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
            ],
            options={
                "verbose_name": "Meal",
                "verbose_name_plural": "Meals",
            },
        ),
        migrations.CreateModel(
            name="MealItem",
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
                ("serving", models.IntegerField(verbose_name="Serving")),
                ("protein", models.FloatField(verbose_name="Protein per serving")),
                ("carbs", models.FloatField(verbose_name="Carbohydrates per serving")),
                ("fats", models.FloatField(verbose_name="Fats per serving")),
                ("total_kcal", models.FloatField(verbose_name="Total kcal")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "food_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="meals.fooditem",
                        verbose_name="Food Item",
                    ),
                ),
                (
                    "meal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="meals.meal",
                        verbose_name="Meal",
                    ),
                ),
            ],
            options={
                "verbose_name": "Meal item",
                "verbose_name_plural": "Meal items",
            },
        ),
        migrations.DeleteModel(
            name="MealPreset",
        ),
    ]
