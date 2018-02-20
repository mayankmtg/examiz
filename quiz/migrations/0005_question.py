# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20180219_2255'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=1000)),
                ('option_a', models.CharField(max_length=250)),
                ('option_b', models.CharField(max_length=250)),
                ('option_c', models.CharField(max_length=250)),
                ('option_d', models.CharField(max_length=250)),
                ('solution', models.CharField(max_length=2)),
                ('assessment', models.ForeignKey(to='quiz.Assessment')),
            ],
        ),
    ]
