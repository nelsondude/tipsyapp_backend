# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-21 06:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocktail', '0002_auto_20170718_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amount',
            name='amount',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='drink',
            name='name',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='drink',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='layer',
            name='layer',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='name',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='playlist_id',
            field=models.CharField(max_length=1000),
        ),
    ]
