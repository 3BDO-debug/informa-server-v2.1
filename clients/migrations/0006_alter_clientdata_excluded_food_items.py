# Generated by Django 4.1.3 on 2023-05-13 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meals", "0014_mealitem_preparation_description_mealitem_video_link"),
        ("clients", "0005_alter_clientdata_water_in_take"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clientdata",
            name="excluded_food_items",
            field=models.ManyToManyField(
                blank=True,
                related_name="excluded_food_items",
                to="meals.fooditem",
                verbose_name="Client excluded food items",
            ),
        ),
    ]
