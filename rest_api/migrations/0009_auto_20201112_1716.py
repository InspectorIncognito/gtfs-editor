# Generated by Django 3.0.7 on 2020-11-12 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0008_auto_20201112_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agency',
            name='agency_timezone',
            field=models.CharField(default='America/Santiago', max_length=20),
            preserve_default=False,
        ),
    ]