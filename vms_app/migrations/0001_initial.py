# Generated by Django 3.1.7 on 2021-04-06 03:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Site",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("street", models.CharField(max_length=100)),
                ("city", models.CharField(max_length=100)),
                ("zip_code", models.CharField(max_length=5, null=True)),
                ("email", models.CharField(max_length=60)),
                ("state", models.CharField(max_length=2, null=True)),
                ("comments", models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Staff",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("last_name", models.CharField(max_length=100)),
                ("first_name", models.CharField(max_length=100)),
                ("phone_number", models.CharField(max_length=40, null=True)),
                ("email", models.CharField(max_length=60)),
                ("password", models.CharField(max_length=60, null=True)),
                ("HIPAACert", models.DateTimeField(blank=True, null=True)),
                ("medical_id", models.IntegerField(blank=True, null=True)),
                ("role", models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name="Station",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("station_name", models.CharField(max_length=100)),
                (
                    "site",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="vms_app.site"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Log",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now=True)),
                ("ipAddress", models.CharField(max_length=40)),
                ("webRequest", models.CharField(max_length=64)),
                ("tableName", models.CharField(max_length=100)),
                ("alteredObject", models.TextField(blank=True)),
                (
                    "staff",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="vms_app.staff"
                    ),
                ),
            ],
        ),
    ]
