# Generated by Django 3.1.7 on 2021-04-15 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vms_app', '0003_patient_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='race',
            field=models.CharField(choices=[('A', 'American Indian/Alaskan Native'), ('S', 'Asian'), ('B', 'Black/African American'), ('P', 'Native Hawaiian/Other Pacific Islander'), ('W', 'White'), ('O', 'Other Race'), ('X', 'Prefer not to specify')], default='X', max_length=8),
        ),
    ]
