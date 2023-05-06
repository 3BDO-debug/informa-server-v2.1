# Generated by Django 4.1.3 on 2023-04-01 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meals", "0010_remove_mealitem_calc_per_piece_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="fooditem",
            name="per_piece_name",
            field=models.CharField(
                blank=True, max_length=350, null=True, verbose_name="Per piece name"
            ),
        ),
    ]
