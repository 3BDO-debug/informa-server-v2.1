# Generated by Django 4.1.3 on 2023-03-12 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("personal_training", "0005_alter_personaltrainingrequest_timestamp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="personaltrainingrequest",
            name="timestamp",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Timestamp"),
        ),
    ]