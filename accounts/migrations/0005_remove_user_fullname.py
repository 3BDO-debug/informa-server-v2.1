# Generated by Django 4.1.3 on 2023-03-08 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_user_fullname"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="fullname",
        ),
    ]
