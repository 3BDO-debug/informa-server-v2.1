# Generated by Django 4.1.3 on 2023-05-16 13:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("support", "0002_supportconversation_supportconversationmessage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="supportconversationmessage",
            name="sender",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="related_sender",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Message's sender",
            ),
        ),
        migrations.CreateModel(
            name="UserSeenMessage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("seen_at", models.DateTimeField(auto_now_add=True)),
                (
                    "message",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="related_message",
                        to="support.supportconversationmessage",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="related_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="supportconversationmessage",
            name="seen_by",
            field=models.ManyToManyField(
                through="support.UserSeenMessage", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
