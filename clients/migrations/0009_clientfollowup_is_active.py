# Generated by Django 4.1.3 on 2023-05-20 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0008_clientfollowup"),
    ]

    operations = [
        migrations.AddField(
            model_name="clientfollowup",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Follow-up is active"),
        ),
    ]