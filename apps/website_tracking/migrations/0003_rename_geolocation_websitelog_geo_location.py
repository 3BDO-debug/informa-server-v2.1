# Generated by Django 4.1.3 on 2023-03-15 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("website_tracking", "0002_websitelog_platform"),
    ]

    operations = [
        migrations.RenameField(
            model_name="websitelog",
            old_name="geolocation",
            new_name="geo_location",
        ),
    ]
