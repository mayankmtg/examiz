# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_timeremaining'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeremaining',
            name='id',
        ),
        migrations.AlterField(
            model_name='timeremaining',
            name='user',
            field=models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
