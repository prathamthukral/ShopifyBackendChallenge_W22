# Generated by Django 3.2.7 on 2021-09-15 03:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoRepoApp', '0002_alter_images_insertedat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='InsertedAt',
            field=models.DateTimeField(verbose_name=datetime.datetime(2021, 9, 15, 3, 51, 45, 232065, tzinfo=utc)),
        ),
    ]
