# Generated by Django 4.1.3 on 2023-01-12 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("programs_generator", "0004_clientdata_prefered_number_of_meals"),
    ]

    operations = [
        migrations.RenameField(
            model_name="clientdata",
            old_name="prefered_number_of_meals",
            new_name="number_of_meals",
        ),
    ]