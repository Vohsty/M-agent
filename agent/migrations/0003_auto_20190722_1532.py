# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-07-22 12:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0002_auto_20190722_1523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='landlord',
            name='email',
        ),
        migrations.RemoveField(
            model_name='landlord',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='landlord',
            name='last_name',
        ),
    ]
