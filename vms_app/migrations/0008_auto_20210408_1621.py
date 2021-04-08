# Generated by Django 3.1.7 on 2021-04-08 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vms_app", "0007_auto_20210408_0412"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dose",
            name="amount",
        ),
        migrations.AddField(
            model_name="vaccinetype",
            name="amount",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
