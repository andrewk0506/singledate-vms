# Generated by Django 3.1.7 on 2021-04-08 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vms_app", "0002_auto_20210408_1401"),
    ]

    operations = [
        migrations.AddField(
            model_name="dose",
            name="notes",
            field=models.TextField(default=""),
        ),
    ]
