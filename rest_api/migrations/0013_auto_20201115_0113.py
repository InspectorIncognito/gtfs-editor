# Generated by Django 3.1.3 on 2020-11-15 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0012_gtfsvalidation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gtfsvalidation',
            old_name='error_message',
            new_name='message',
        ),
    ]