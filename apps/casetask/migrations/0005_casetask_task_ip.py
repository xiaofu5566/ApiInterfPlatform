# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-08-21 19:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casetask', '0004_caseresults'),
    ]

    operations = [
        migrations.AddField(
            model_name='casetask',
            name='task_ip',
            field=models.CharField(default='', max_length=30, verbose_name='\u6267\u884c\u4efb\u52a1\u73af\u5883ip'),
        ),
    ]
