# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-09 15:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('depart', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('trips', models.ManyToManyField(related_name='all_trips', to='exam.User')),
                ('user_trips', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_trips', to='exam.User')),
            ],
        ),
    ]
