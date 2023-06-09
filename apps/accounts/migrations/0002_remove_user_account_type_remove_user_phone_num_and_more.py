# Generated by Django 4.1.3 on 2023-03-08 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="account_type",
        ),
        migrations.RemoveField(
            model_name="user",
            name="phone_num",
        ),
        migrations.RemoveField(
            model_name="user",
            name="profile_pic",
        ),
        migrations.AddField(
            model_name="user",
            name="allowed_views",
            field=models.CharField(
                max_length=350, null=True, verbose_name="Allowed Views"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(max_length=350, null=True, verbose_name="Role"),
        ),
    ]
