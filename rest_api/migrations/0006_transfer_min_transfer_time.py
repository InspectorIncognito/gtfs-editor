# Generated by Django 3.0.7 on 2020-11-11 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0005_auto_20201111_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfer',
            name='min_transfer_time',
            field=models.IntegerField(null=True),
        ),
    ]