# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-25 06:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backweb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodtype',
            name='type_img',
            field=models.CharField(max_length=200),
        ),
    ]
