# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-02-05 02:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.SmallIntegerField(choices=[(2, 'aprovado'), (3, 'deshabilitado'), (1, 'pending')], default=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Name of User'),
        ),
    ]
