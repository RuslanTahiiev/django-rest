# Generated by Django 3.2.9 on 2021-11-11 12:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteupdatenews',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 11, 14, 24, 59, 568312)),
        ),
        migrations.AlterField(
            model_name='siteupdatenews',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
