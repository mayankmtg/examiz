# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_assessment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
