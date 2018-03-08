# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_auto_20180308_0655'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeremaining',
            name='assessment',
            field=models.ForeignKey(default=None, to='quiz.Assessment'),
        ),
    ]
