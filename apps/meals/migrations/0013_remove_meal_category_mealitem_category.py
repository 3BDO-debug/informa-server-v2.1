# Generated by Django 4.1.3 on 2023-04-04 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meals", "0012_remove_fooditem_category_meal_category"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="meal",
            name="category",
        ),
        migrations.AddField(
            model_name="mealitem",
            name="category",
            field=models.CharField(
                default="category", max_length=350, verbose_name="Category"
            ),
            preserve_default=False,
        ),
    ]
