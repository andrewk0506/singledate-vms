# Generated by Django 3.1.7 on 2021-04-02 23:36

from django.db import migrations, models
import vms_app.models.utils


class Migration(migrations.Migration):

    dependencies = [
        ('vms_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalelgibility',
            name='gender',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('X', 'Non binary')], default=vms_app.models.utils.Gender['F'], max_length=1),
        ),
    ]
