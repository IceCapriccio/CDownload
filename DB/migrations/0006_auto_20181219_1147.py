# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-19 03:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DB', '0005_downloadlog_downloadtimes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='passwor',
            new_name='password',
        ),
    ]