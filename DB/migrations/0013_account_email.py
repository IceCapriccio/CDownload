# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-20 11:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DB', '0012_auto_20181220_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='email',
            field=models.CharField(max_length=30, null=True),
        ),
    ]