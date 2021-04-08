# Generated by Django 3.1.7 on 2021-04-08 18:01

from django.db import migrations, models
import django.db.models.deletion
import vms_app.models.utils


class Migration(migrations.Migration):

    dependencies = [
        ('vms_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicaleligibilityanswer',
            name='person',
        ),
        migrations.AddField(
            model_name='role',
            name='site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vms_app.site'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='address_type',
            field=models.CharField(choices=[('H', 'Home'), ('C', 'Current/Temporary'), ('P', 'Permanet'), ('M', 'Mailing')], default=vms_app.models.utils.AddressType['H'], max_length=1),
        ),
        migrations.AlterField(
            model_name='patient',
            name='ethnicity',
            field=models.CharField(choices=[('H', 'Hispanic'), ('N', 'Non-hispanic'), ('X', 'Prefer not to specify')], default=vms_app.models.utils.Ethnicity['X'], max_length=1),
        ),
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('X', 'Non binary')], default=vms_app.models.utils.Gender['F'], max_length=1),
        ),
        migrations.AlterField(
            model_name='patient',
            name='race',
            field=models.CharField(choices=[('A', 'American Indian/Alaskan Native'), ('S', 'Asian'), ('B', 'Black/African American'), ('P', 'Native Hawaiian/Other Pacific Islander'), ('W', 'White'), ('O', 'Other Race'), ('X', 'Prefer not to specify')], default=vms_app.models.utils.Race['X'], max_length=1),
        ),
        migrations.AlterField(
            model_name='patient',
            name='state',
            field=models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], default=vms_app.models.utils.States['NJ'], max_length=2),
        ),
        migrations.AlterField(
            model_name='role',
            name='role',
            field=models.CharField(choices=[('A', 'ADMIN'), ('V', 'VACCINATOR'), ('S', 'SUPPORT STAFF')], default=None, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='station',
            name='stationName',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('ipAddress', models.CharField(max_length=40)),
                ('webRequest', models.CharField(max_length=64)),
                ('tableName', models.CharField(max_length=100)),
                ('alteredObject', models.TextField(blank=True)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vms_app.staff')),
            ],
        ),
    ]
