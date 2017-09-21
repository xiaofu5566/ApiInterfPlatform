#-*- coding:utf-8 -*-
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render,redirect
from django.views.generic.base import View
from datetime import datetime
from django.http import HttpResponse
import json

from .models import CaseTask,ResultReport
from common.common import InitScOrSt

#测试任务管理列表页
class CaseTaskListView(View):
    def get(self,request):
        casetasks = CaseTask.objects.all()
        #对任务列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # Provide Paginator with the request object for complete querystring generation
        p = Paginator(casetasks,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        casetasklist = p.page(page)
        return render(request,"taskManage.html",{"casetasklist":casetasklist})


#新增测试任务
class AddTskView(View):
    def post(self,request):
        task_name = request.POST.get("taskname")
        exec_plan = request.POST.get("plan")
        prj_name = request.POST.get("prj")
        case_id = request.POST.get("caseid")
        task_ip = request.POST.get("taskip")
        updatetime = datetime.now()

        casetsk = CaseTask()
        casetsk.task_name = task_name
        casetsk.exec_plan = exec_plan
        casetsk.prj_name = prj_name
        casetsk.case_id = case_id
        casetsk.task_ip = task_ip
        casetsk.updatetime = updatetime
        casetsk.author = request.user.username
        casetsk.save()

        casetasks = CaseTask.objects.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(casetasks,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        casetasklist = p.page(page)
        return render(request,"taskManage.html",{"casetasklist":casetasklist})

#修改测试任务
class AlterTaskView(View):
    def get(self,request):
        casetasks = CaseTask.objects.all()
        #对任务列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # Provide Paginator with the request object for complete querystring generation
        p = Paginator(casetasks,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        casetasklist = p.page(page)
        return render(request,"taskManage.html",{"casetasklist":casetasklist})

    def post(self,request):
        taskid = request.POST.get("alprjid")
        task_ip = request.POST.get("altaskip")
        task_name = request.POST.get("altaskname")
        exec_plan = request.POST.get("alplan")
        prj_name = request.POST.get("alprj")
        case_id = request.POST.get("alcaseid")
        updatetime = datetime.now()

        casetsk = CaseTask.objects.get(id=taskid)
        casetsk.task_name = task_name
        casetsk.task_ip = task_ip
        casetsk.exec_plan = exec_plan
        casetsk.prj_name = prj_name
        casetsk.case_id = case_id
        casetsk.updatetime = updatetime
        casetsk.author = request.user.username
        casetsk.save()

        casetasks = CaseTask.objects.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(casetasks,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        casetasklist = p.page(page)
        return render(request,"taskManage.html",{"casetasklist":casetasklist})


#初始化测试任务修改页面
class InitTaskView(View):
    def get(self,request):
        taskid = request.GET.get("prjidval")
        task = CaseTask.objects.get(id=taskid)
        task_name = task.task_name
        exec_plan = task.exec_plan
        prj_name = task.prj_name
        case_id = task.case_id
        task_ip = task.task_ip
        content = {"taskname":task_name,"execplan":exec_plan,"prjname":prj_name,"caseid":case_id,"taskip":task_ip}
        return HttpResponse(json.dumps(content))

#删除测试任务
class DeleTaskView(View):
    def get(self,request,taskid):
        task = CaseTask.objects.get(id=taskid)
        task.delete()

        casetasks = CaseTask.objects.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(casetasks,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        casetasklist = p.page(page)
        return render(request,"taskManage.html",{"casetasklist":casetasklist})

#查询任务
class SearchTaskView(View):
    def get(self,request,taskname):
        if taskname=="null":
            casetasks = CaseTask.objects.all()
        else:
            casetasks = CaseTask.objects.filter(task_name__icontains=taskname)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(casetasks,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        casetasklist = p.page(page)
        return render(request,"taskManage.html",{"casetasklist":casetasklist})

#测试报告列表
class RsReportListView(View):
    print 'test'
    def get(self,request):
        rsrlist = ResultReport.objects.all()
        #对测试报告列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # Provide Paginator with the request object for complete querystring generation
        p = Paginator(rsrlist,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        reportlist = p.page(page)
        return render(request,"resultManage.html",{"reportlist":reportlist})

#删除测试报告
class DeleReportView(View):
    def get(self,request,repid):
        rsr = ResultReport.objects.get(id=int(repid))
        rsr.delete()
        rsrlist = ResultReport.objects.all()
        #对测试报告列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # Provide Paginator with the request object for complete querystring generation
        p = Paginator(rsrlist,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        reportlist = p.page(page)
        return render(request,"resultManage.html",{"reportlist":reportlist})

#查询测试报告
class SearchReptView(View):
    def get(self,request,taskname):
        if taskname == "null":
            rsrlist = ResultReport.objects.all()
        else:
            rsrlist = ResultReport.objects.filter(taskid__task_name=taskname)
        #对测试报告列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # Provide Paginator with the request object for complete querystring generation
        p = Paginator(rsrlist,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        reportlist = p.page(page)
        return render(request,"resultManage.html",{"reportlist":reportlist})


#初始化积分或库存view
class InitDataView(View):
    def post(self,request):
        type = request.POST.get("datatype")
        envir = request.POST.get("envirmt")
        scoreorstock = request.POST.get("scoreorstock")
        data = int(scoreorstock)
        #初始化积分或库存方法
        InitScOrSt(envir,type,data)

        casetasks = CaseTask.objects.all()
        #对任务列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # Provide Paginator with the request object for complete querystring generation
        p = Paginator(casetasks,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        casetasklist = p.page(page)
        return render(request,"taskManage.html",{"casetasklist":casetasklist})






