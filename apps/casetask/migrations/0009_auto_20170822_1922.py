# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-08-22 19:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casetask', '0008_auto_20170822_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caseresults',
            name='realresult',
            field=models.TextField(max_length=3000, verbose_name='\u5b9e\u9645\u7ed3\u679c'),
        ),
    ]
