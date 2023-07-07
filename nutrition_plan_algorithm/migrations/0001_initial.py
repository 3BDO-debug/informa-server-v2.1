# Generated by Django 4.1.3 on 2023-05-07 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("clients", "0001_initial"),
        ("meals", "0014_mealitem_preparation_description_mealitem_video_link"),
    ]

    operations = [
        migrations.CreateModel(
            name="NutritionPlan",
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
                    "schema",
                    models.CharField(
                        max_length=350, verbose_name="Nutrition plan generation schema"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=False, verbose_name="Plan is active"),
                ),
                (
                    "generated_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Generated at"
                    ),
                ),
                (
                    "client_data",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="clients.clientdata",
                        verbose_name="Related client data",
                    ),
                ),
            ],
            options={
                "verbose_name": "Nutrition plan",
                "verbose_name_plural": "Nutrition plans",
            },
        ),
        migrations.CreateModel(
            name="NutritionPlanMeal",
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
                    "meal_index",
                    models.CharField(max_length=350, verbose_name="Meal index"),
                ),
                (
                    "meal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="meals.meal",
                        verbose_name="Related Meal",
                    ),
                ),
                (
                    "nutrition_plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="nutrition_plan_algorithm.nutritionplan",
                        verbose_name="Related nutrition plan",
                    ),
                ),
            ],
            options={
                "verbose_name": "Nutrition plan meal",
                "verbose_name_plural": "Nutrition plans meals",
            },
        ),
        migrations.CreateModel(
            name="NutritionPlanMealItem",
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
                    "replaced",
                    models.BooleanField(
                        default=False, verbose_name="Replaced meal item"
                    ),
                ),
                (
                    "meal_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="meals.mealitem",
                        verbose_name="Related meal item",
                    ),
                ),
                (
                    "nutrition_plan_meal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="nutrition_plan_algorithm.nutritionplanmeal",
                        verbose_name="Related nutrition plan meal",
                    ),
                ),
                (
                    "replaced_with",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replaced_meal_items",
                        to="meals.fooditem",
                        verbose_name="Replaced meal item with",
                    ),
                ),
            ],
            options={
                "verbose_name": "Nutrition plan meal item",
                "verbose_name_plural": "Nutrition plans meal items",
            },
        ),
    ]