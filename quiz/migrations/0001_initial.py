# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('date', models.DateTimeField()),
                ('max_marks', models.IntegerField()),
                ('no_of_questions', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('description', models.CharField(max_length=2000, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=1000)),
                ('option_a', models.CharField(max_length=250)),
                ('option_b', models.CharField(max_length=250)),
                ('option_c', models.CharField(max_length=250)),
                ('option_d', models.CharField(max_length=250)),
                ('question_image', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('option_a_image', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('option_b_image', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('option_c_image', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('option_d_image', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('solution', models.CharField(max_length=2)),
                ('assessment', models.ForeignKey(to='quiz.Assessment')),
            ],
        ),
        migrations.CreateModel(
            name='registerRequests',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('e_mail', models.CharField(max_length=250)),
                ('password', models.CharField(max_length=250)),
                ('confirm_password', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('response', models.CharField(max_length=2)),
                ('assessment', models.ForeignKey(to='quiz.Assessment')),
                ('question', models.ForeignKey(to='quiz.Question')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='timeRemaining',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timeStart', models.DateTimeField()),
                ('timeEnd', models.DateTimeField()),
                ('assessment', models.ForeignKey(to='quiz.Assessment')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
