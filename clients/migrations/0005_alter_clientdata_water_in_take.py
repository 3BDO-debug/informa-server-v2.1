# Generated by Django 4.1.3 on 2023-05-13 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0004_clientdata_water_in_take"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clientdata",
            name="water_in_take",
            field=models.FloatField(verbose_name="Daily water in take"),
        ),
    ]
