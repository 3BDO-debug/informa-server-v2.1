# Generated by Django 4.1.3 on 2023-06-15 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("workout_plan_algorithm", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="workout",
            name="complexity",
        ),
        migrations.DeleteModel(
            name="WorkoutLevel",
        ),
    ]