# Generated by Django 3.2.9 on 2021-11-11 14:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0002_auto_20211111_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteupdatenews',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 11, 16, 1, 25, 896269)),
        ),
        migrations.AlterField(
            model_name='siteupdatenews',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
