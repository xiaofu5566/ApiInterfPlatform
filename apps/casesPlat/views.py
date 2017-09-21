#-*- coding:utf-8 -*-
from itertools import chain
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render
from django.views.generic.base import View
from datetime import datetime
from django.http import HttpResponse
import json

from .models import InterCases
from interfcacePlat.models import Interfaces,Projects


# Create your views here.
#接口用例管理页面列表显示
class CasesListView(View):
    def get(self,request):
        intefcases_all =  InterCases.objects.all()
        #对项目数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(intefcases_all,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        intefcaseslist = p.page(page)
        return render(request,"caseManage.html",{"intefcaseslist":intefcaseslist})

#新增用例
class AddCasesView(View):
    def get(self,request):
        intefcases_all =  InterCases.objects.all()
        #对项目数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(intefcases_all,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        intefcaseslist = p.page(page)
        return render(request,"caseManage.html",{"intefcaseslist":intefcaseslist})
    def post(self,request):
        casename = request.POST.get("casename")
        precondition = request.POST.get("precondition")
        headinfo = request.POST.get("headinf")
        param = request.POST.get("parms")
        expectRs = request.POST.getlist("expectrs") #多个预期结果
        exrsnums = len(expectRs)
        expectRs_save = ""
        #用字符串的方式存储预期结果，用分号分割多个预期结果
        for i in range(len(expectRs)):
            if i<len(expectRs)-1:
                expectRs_save = expectRs_save+expectRs[i]+";"
            elif i==len(expectRs)-1:
                expectRs_save = expectRs_save+expectRs[i]

        interid = request.POST.get("interid")
        updatetime =datetime.now()

        interfaceCase = InterCases()
        interfaceCase.casename = casename
        interfaceCase.precondition = precondition
        interfaceCase.headinfo = headinfo
        interfaceCase.expectRs = expectRs_save
        interfaceCase.expectRs_nums = exrsnums
        interfaceCase.interid_id= interid
        interfaceCase.updatetime = updatetime
        interfaceCase.author = request.user.username
        interfaceCase.save()

        intefcases_all =  InterCases.objects.all()
        #对项目数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(intefcases_all,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        intefcaseslist = p.page(page)
        return render(request,"caseManage.html",{"intefcaseslist":intefcaseslist})

#修改用例
class AlterCaseView(View):
    def get(self,request):
        intefcases_all =  InterCases.objects.all()
        #对项目数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(intefcases_all,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        intefcaseslist = p.page(page)
        return render(request,"caseManage.html",{"intefcaseslist":intefcaseslist})
    def post(self,request):
        recordid = request.POST.get("alprjid")
        headinf = request.POST.get("alheadinf")
        alparms = request.POST.get("alparms")
        alcasename = request.POST.get("alcasename")
        alprecondition = request.POST.get("alprecondition")
        alexpectrs = request.POST.getlist("alexpectrs")
        exrsnums = len(alexpectrs)
        expectRs_save = ""
        #用字符串的方式存储预期结果，用分号分割多个预期结果
        for i in range(len(alexpectrs)):
            if i<len(alexpectrs)-1:
                expectRs_save = expectRs_save+alexpectrs[i]+";"
            elif i==len(alexpectrs)-1:
                expectRs_save = expectRs_save+alexpectrs[i]

        case = InterCases.objects.get(id=int(recordid))
        case.casename = alcasename
        case.headinfo = headinf
        case.param = alparms
        case.precondition = alprecondition
        case.expectRs = expectRs_save
        case.expectRs_nums = exrsnums
        case.author = request.user.username
        case.save()

        intefcases_all =  InterCases.objects.all()
        #对项目数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(intefcases_all,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        intefcaseslist = p.page(page)
        return render(request,"caseManage.html",{"intefcaseslist":intefcaseslist})

#联动查询uri
class SearchUriView(View):
    def get(self,request):
        modname = request.GET.get("modname")
        interfaces = Interfaces.objects.filter(projectId__module_name=modname)
        uris = []
        for i in interfaces:
            uris.append(i.interf_url)
        content = {"uris":uris}
        return HttpResponse(json.dumps(content))

#根据uri自动带出接口方法，头信息，请求参数
class SearchMhpView(View):
    def get(self,request):
        uri = request.GET.get("uri")
        interface = Interfaces.objects.get(interf_url=uri)
        content ={"method":interface.interf_method,"headinf":interface.interf_header,"parms":interface.interf_param,"interid":interface.id}
        return HttpResponse(json.dumps(content))

#初始化修改用例页面数据
class InitCasesView(View):
    def get(self,request):
        caseid = request.GET.get("prjidval")
        case = InterCases.objects.get(id=int(caseid))
        interf = Interfaces.objects.get(id=case.interid_id)

        prjname = Projects.objects.get(id=interf.projectId_id).project_name
        modname = Projects.objects.get(id=interf.projectId_id).module_name
        uri = interf.interf_url
        method = interf.interf_method
        headinf = case.headinfo
        parm = case.param
        casename = case.casename
        precondtion = case.precondition
        expectrs = case.expectRs
        expectrs_show = expectrs.split(';')

        expectrs_nums = case.expectRs_nums

        showIntf = [prjname,modname,uri,method,headinf,parm,casename,precondtion]

        content = {"interf_start":showIntf,"expectrs":expectrs_show,'expectrs_nums':expectrs_nums}
        return HttpResponse(json.dumps(content))

#查询接口测试用例
class SearchCasesView(View):
    def get(self,request,sprj,smod,casepath):
         #查询全部数据
        if sprj =="null" and (smod=="null" or smod==None) and casepath=="null" :
            all_interf_cases = InterCases.objects.all()
        #根据接口path查询用例
        elif casepath!="null":
            all_interfaces = Interfaces.objects.filter(interf_url__icontains=casepath)
            #空queryset
            all_interf_cases = InterCases.objects.none()
            for intf in all_interfaces:
                cases = InterCases.objects.filter(interid_id=intf.id)
                all_interf_cases = all_interf_cases|cases
        #查询项目下的接口用例
        elif sprj !="null" and smod=="null":
            all_interfaces = Interfaces.objects.filter(projectId__project_name=sprj)
            #空queryset
            all_interf_cases = InterCases.objects.none()
            for intf in all_interfaces:
                cases = InterCases.objects.filter(interid_id=intf.id)
                all_interf_cases = all_interf_cases|cases
        #查询模块下的接口
        elif sprj !="null" and smod !="null":
            all_interfaces = Interfaces.objects.filter(projectId__project_name=sprj,projectId__module_name=smod )
            #空queryset
            all_interf_cases = InterCases.objects.none()
            for intf in all_interfaces:
                cases = InterCases.objects.filter(interid_id=intf.id)
                all_interf_cases = all_interf_cases|cases
         #对接口用例数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_interf_cases,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        intefcaseslist = p.page(page)
        return render(request,"caseManage.html",{"intefcaseslist":intefcaseslist})

#删除用例
class Del_caseView(View):
    def get(self,request,caseid):
        InterCases.objects.filter(id=caseid).delete()
        all_interf_cases = InterCases.objects.all()
        #对接口用例数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_interf_cases,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        intefcaseslist = p.page(page)
        return render(request,"caseManage.html",{"intefcaseslist":intefcaseslist})













