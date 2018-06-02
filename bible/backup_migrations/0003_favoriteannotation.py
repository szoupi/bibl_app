# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-05-16 17:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bible', '0002_auto_20180516_1711'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteAnnotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bible.Annotation', verbose_name=b'Annotation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'User')),
            ],
            options={
                'db_table': 'favorite_annotation',
            },
        ),
    ]