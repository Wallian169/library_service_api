# Generated by Django 5.1.1 on 2024-09-26 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
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
                ("title", models.CharField(max_length=255)),
                ("author", models.CharField(max_length=255)),
                (
                    "cover",
                    models.CharField(
                        choices=[("HARD", "Hard"), ("SOFT", "Soft")], max_length=4
                    ),
                ),
                ("inventory", models.PositiveSmallIntegerField(default=1)),
                ("daily_fee", models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
