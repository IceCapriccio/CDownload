# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-19 05:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DB', '0007_auto_20181219_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='permission',
            field=models.CharField(default='user', max_length=5),
        ),
    ]
