#-*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

from interfcacePlat.models import Interfaces

# Create your models here.
# 接口用例model
class InterCases(models.Model):
    casename = models.CharField(max_length=50,verbose_name="用例名称")
    precondition = models.CharField(max_length=30,verbose_name="前提用例")
    headinfo = models.CharField(max_length=3000,verbose_name="头信息")
    param = models.CharField(max_length=3000,verbose_name="请求参数")
    expectRs = models.CharField(max_length=3000,verbose_name="预期结果")
    expectRs_nums = models.IntegerField(verbose_name=u"预期结果数量",default=0)
    interid = models.ForeignKey(Interfaces,verbose_name="接口")
    updatetime = models.DateTimeField(default=datetime.now)
    author = models.CharField(max_length=10,verbose_name=u"操作人",default="")