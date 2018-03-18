# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_timeremaining_assessment'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='option_a_image',
            field=models.CharField(default=None, max_length=250),
        ),
        migrations.AddField(
            model_name='question',
            name='option_b_image',
            field=models.CharField(default=None, max_length=250),
        ),
        migrations.AddField(
            model_name='question',
            name='option_c_image',
            field=models.CharField(default=None, max_length=250),
        ),
        migrations.AddField(
            model_name='question',
            name='option_d_image',
            field=models.CharField(default=None, max_length=250),
        ),
        migrations.AddField(
            model_name='question',
            name='question_image',
            field=models.CharField(default=None, max_length=250),
        ),
    ]
