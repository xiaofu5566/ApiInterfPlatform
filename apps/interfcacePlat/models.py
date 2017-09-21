#-*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models

# Create your models here.

#接口模块
class Projects(models.Model):
    project_name = models.CharField(max_length=10,verbose_name=u"项目名")
    module_name = models.CharField(max_length=50,verbose_name=u"模块名")
    updatetime = models.DateTimeField(default=datetime.now)
    author = models.CharField(max_length=10,verbose_name=u"操作人")


#接口
class Interfaces(models.Model):
    projectId = models.ForeignKey(Projects,verbose_name=u"所属项目",related_name="PROM")
    interf_url = models.CharField(max_length=50,verbose_name=u"接口url")
    interf_header = models.CharField(max_length=3000,verbose_name=u"头信息")
    interf_method = models.CharField(max_length=10,verbose_name=u"方法")
    interf_param = models.CharField(max_length=3000,verbose_name=u"参数")
    updatetime = models.DateTimeField(default=datetime.now)
    author = models.CharField(max_length=10,verbose_name=u"操作人")