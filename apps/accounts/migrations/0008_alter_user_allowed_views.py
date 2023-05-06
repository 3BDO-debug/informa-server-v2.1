# Generated by Django 4.1.3 on 2023-05-06 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_alter_user_allowed_views"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="allowed_views",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                to="accounts.allowedview",
                verbose_name="Allowed Views",
            ),
        ),
    ]
