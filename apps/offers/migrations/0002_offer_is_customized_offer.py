# Generated by Django 4.1.3 on 2023-03-15 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("offers", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="offer",
            name="is_customized_offer",
            field=models.BooleanField(
                default=False, verbose_name="Is customized offer ?"
            ),
        ),
    ]
