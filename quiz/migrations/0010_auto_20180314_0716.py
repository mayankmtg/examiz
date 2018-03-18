# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_auto_20180314_0715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='option_a_image',
            field=models.CharField(default=None, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='option_b_image',
            field=models.CharField(default=None, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='option_c_image',
            field=models.CharField(default=None, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='option_d_image',
            field=models.CharField(default=None, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_image',
            field=models.CharField(default=None, max_length=250, null=True),
        ),
    ]
