# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-26 20:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('examapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='plan_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='planusers', to='examapp.User'),
        ),
    ]
