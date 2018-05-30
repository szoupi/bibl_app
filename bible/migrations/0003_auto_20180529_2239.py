# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-05-29 22:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bible', '0002_auto_20180529_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoriteannotation',
            name='obj',
            field=models.ForeignKey(default=b'', on_delete=django.db.models.deletion.CASCADE, to='bible.Annotation', verbose_name=b'Annotation'),
        ),
        migrations.AlterField(
            model_name='favoritechapter',
            name='obj',
            field=models.ForeignKey(default=b'', on_delete=django.db.models.deletion.CASCADE, to='bible.Chapter', verbose_name=b'Chapter'),
        ),
        migrations.AlterField(
            model_name='favoriteverse',
            name='obj',
            field=models.ForeignKey(default=b'', on_delete=django.db.models.deletion.CASCADE, to='bible.Verse', verbose_name=b'Verse'),
        ),
    ]
