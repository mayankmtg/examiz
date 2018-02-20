# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_remove_registerrequests_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('max_marks', models.IntegerField()),
                ('no_of_questions', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('description', models.CharField(max_length=2000, blank=True)),
            ],
        ),
    ]
