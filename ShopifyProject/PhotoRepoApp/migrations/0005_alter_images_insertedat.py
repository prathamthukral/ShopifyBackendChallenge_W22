# Generated by Django 3.2.7 on 2021-09-15 04:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoRepoApp', '0004_alter_images_insertedat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='InsertedAt',
            field=models.DateTimeField(verbose_name=datetime.datetime(2021, 9, 15, 4, 0, 4, 834564, tzinfo=utc)),
        ),
    ]
