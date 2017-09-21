#-*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models

from casesPlat.models import InterCases

#测试任务model
class CaseTask(models.Model):
    task_name = models.CharField(max_length=30,verbose_name=u"任务名称")
    task_ip = models.CharField(max_length=30,verbose_name=u"执行任务环境ip", default="")
    exec_plan = models.CharField(max_length=10,verbose_name=u"测试方案")
    prj_name = models.CharField(max_length=30,verbose_name=u"项目名",default="")
    case_id = models.CharField(max_length=300,verbose_name=u"用例id",default="")
    updatetime = models.DateTimeField(default=datetime.now)
    author = models.CharField(max_length=10,verbose_name=u"操作人",default="admin")

#测试结果集model
class CaseResults(models.Model):
    taskid =  models.IntegerField(verbose_name=u"任务id")
    caseid =  models.ForeignKey(InterCases,verbose_name=u"测试用例")
    realresult =  models.TextField(max_length=3000,verbose_name=u"实际结果")
    istrue = models.IntegerField(choices=((0,"通过"),(1,"不通过"),(2,"未执行")),verbose_name=u"是否通过",default=2)
    flag = models.CharField(max_length=100,verbose_name=u"结果批次",default="")
    updatetime = models.DateTimeField(default=datetime.now,verbose_name=u"执行时间")
    author = models.CharField(max_length=10,verbose_name=u"操作人",default="admin")

#测试报告
class ResultReport(models.Model):
    name = models.CharField(max_length=50,verbose_name=u"测试报告名")
    taskid = models.ForeignKey(CaseTask,verbose_name=u"测试任务")
    failnum = models.IntegerField(verbose_name=u"失败数")
    nums = models.IntegerField(verbose_name=u"总用例数",default=0)
    durt = models.IntegerField(verbose_name=u"测试时长")
    flag = models.CharField(max_length=100,verbose_name=u"结果批次",default="")
    creattime = models.DateTimeField(default=datetime.now,verbose_name=u"创建时间")