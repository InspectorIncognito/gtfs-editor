# Generated by Django 3.1.3 on 2021-02-10 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0024_stoptimes_time_format'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedinfo',
            name='feed_contact_email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='feedinfo',
            name='feed_contact_url',
            field=models.URLField(null=True),
        ),
    ]