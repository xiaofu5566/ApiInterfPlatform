#-*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth import authenticate,login
from django.contrib import auth
from django.shortcuts import render,redirect
from django.views.generic.base import View
from datetime import datetime
from django.http import HttpResponse
import json

from .interform import ProjForm
from .models import Projects,Interfaces
# Create your views here.


class BaseView(View):
    def get(self,request):
        return render(request,'base.html')
#项目列表
class ProjListView(View):
    def get(self,request):
        projmods_all = Projects.objects.all()
        #对项目数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # Provide Paginator with the request object for complete querystring generation
        p = Paginator(projmods_all,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        projmods = p.page(page)
        return render(request,"proj.html",{"projmods":projmods,"projmodall":projmods_all})

  #新增项目模块
class AddPrjView(View):
    def get(self,request):
        projmods_all = Projects.objects.all()
        #对项目数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(projmods_all,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        projmods = p.page(page)
        return render(request,"proj.html",{"projmods":projmods})
    def post(self,request):
        prjid = request.POST.get("prjid")
        prjname = request.POST.get("prj")
        modname = request.POST.get("mod")
        username= request.user.username
        #新增项目模块
        projmod = Projects()
        projmod.project_name = prjname
        projmod.module_name = modname
        projmod.updatetime = datetime.now()
        projmod.author = username
        projmod.save()
        projmods_all = Projects.objects.all()
        #对项目数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(projmods_all,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        projmods = p.page(page)
        return render(request,"proj.html",{"projmods":projmods})

#修改项目模块
class AlterPrjView(View):
    def get(self,request):
        projmods_all = Projects.objects.all()
        #对项目数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(projmods_all,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        projmods = p.page(page)
        return render(request,"proj.html",{"projmods":projmods})
    def post(self,request):
        prjid = request.POST.get('prjid')
        prjname = request.POST.get('alprj')
        modname = request.POST.get('almod')
        #修改项目模块
        projmod = Projects.objects.get(id=int(prjid))
        projmod.project_name = prjname
        projmod.module_name = modname
        projmod.updatetime = datetime.now()
        projmod.author = request.user.username
        projmod.save()

        projmods_all = Projects.objects.all()
        #对项目数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(projmods_all,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        projmods = p.page(page)
        return render(request,"proj.html",{"projmods":projmods})

#删除项目模块
class DelPrjView(View):
    def get(self,request,prjid):
        Projects.objects.filter(id=int(prjid)).delete()
        projmods_all = Projects.objects.all()
        #对项目数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(projmods_all,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        projmods = p.page(page)
        return render(request,"proj.html",{"projmods":projmods})

#初始化项目模块修改页面数据
class ShowPrjView(View):
    def get(self,request):
        prjid = request.GET.get('prjidval')
        prjmod = Projects.objects.get(id=int(prjid))
        content = {"prjname":prjmod.project_name,"mod":prjmod.module_name}
        return HttpResponse(json.dumps(content))


#查询项目模块数据
class SearcView(View):
    def get(self,request,prj,mod):
        if prj=='null' and mod!='null':
            projmods_all = Projects.objects.filter(module_name=mod)
        elif prj=='null' and mod=='null':
            projmods_all = Projects.objects.all()
        elif prj!='null' and mod=='null':
            projmods_all = Projects.objects.filter(project_name=prj)
        else:
            projmods_all = Projects.objects.filter(project_name=prj,module_name=mod)
        #对项目数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(projmods_all,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        projmods = p.page(page)
        return render(request,"proj.html",{"projmods":projmods})

#接口列表
class InterfListView(View):
    def get(self,request):
        all_interfaces = Interfaces.objects.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_interfaces,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        interfaces = p.page(page)
        return render(request,"interfaceManage.html",{"interfaces":interfaces})

#添加接口
class AddInterView(View):
    def get(self,request):
        all_interfaces = Interfaces.objects.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_interfaces,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        interfaces = p.page(page)
        return render(request,"interfaceManage.html",{"interfaces":interfaces})

    def post(self,request):
        prjname = request.POST.get('addprj')
        prjmod = request.POST.get('mod')
        #获取外键id
        project = Projects.objects.filter(project_name=prjname,module_name=prjmod)
        for pro in project:
            projectid = pro.id

        interf_url = request.POST.get('url')
        interf_header = request.POST.get('headinf')
        interf_method = request.POST.get('inmethod')
        interf_param = request.POST.get('inparm')
        interf = Interfaces()
        interf.projectId_id = projectid
        interf.interf_url = interf_url
        interf.interf_header = interf_header
        interf.interf_method = interf_method
        interf.interf_param = interf_param
        interf.updatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        interf.save()
        all_interfaces = Interfaces.objects.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_interfaces,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        interfaces = p.page(page)
        return render(request,"interfaceManage.html",{"interfaces":interfaces})


#根据项目返回对应的模块name列表
class ModListView(View):
    def get(self,request):
        prjname = request.GET.get("prjname")
        prjmod = Projects.objects.filter(project_name=prjname)
        prjmod_name = []
        for pm in prjmod:
            prjmod_name.append(pm.module_name)
        content = {"prjmod_name":prjmod_name}
        return HttpResponse(json.dumps(content))

#修改接口
class AlterInterfaceView(View):
    def get(self,request):
        all_interfaces = Interfaces.objects.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_interfaces,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        interfaces = p.page(page)
        return render(request,"interfaceManage.html",{"interfaces":interfaces})
    def post(self,request):
        #获取要修改的数据id
        alprjid = request.POST.get('alprjid')

        prjname = request.POST.get('alprj')
        prjmod = request.POST.get('almod')
        #获取外键id
        project = Projects.objects.get(project_name=prjname,module_name=prjmod)
        projectid = project.id

        interf_url = request.POST.get('alurl')
        interf_header = request.POST.get('alheadinf')
        interf_method = request.POST.get('alinmethod')
        interf_param = request.POST.get('alinparm')

        interf = Interfaces.objects.get(id=int(alprjid))
        interf.projectId_id = projectid
        interf.interf_url = interf_url
        interf.interf_header = interf_header
        interf.interf_method = interf_method
        interf.interf_param = interf_param
        interf.updatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        interf.save()
        all_interfaces = Interfaces.objects.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_interfaces,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        interfaces = p.page(page)
        return render(request,"interfaceManage.html",{"interfaces":interfaces})

#修改接口页面初始化时显示的数据
class ShowInterfView(View):
    def get(self,request):
        id = request.GET.get("prjidval")
        interface = Interfaces.objects.get(id=int(id))
        projectid = interface.projectId_id
        project = Projects.objects.get(id=projectid)
        project_name = project.project_name
        module_name = project.module_name
        #根据项目名查找该项目下所有的模块
        pro_mod_name = Projects.objects.filter(project_name=project_name)
        all_module_name = []
        for pmn in pro_mod_name:
            all_module_name.append(pmn.module_name)

        interf_url = interface.interf_url
        interf_header = interface.interf_header
        interf_method = interface.interf_method
        interf_param = interface.interf_param
        showIntf = [project_name,module_name,interf_url,interf_header,interf_method,interf_param,all_module_name]
        content = {"interf_start":showIntf}
        return HttpResponse(json.dumps(content))

#删除接口
class Del_IntefView(View):
    def get(self,request,delid):
        try:
            del_interface = Interfaces.objects.get(id=int(delid))
            if del_interface:
                del_interface.delete()
        except Exception as e:
            print e.message

        all_interfaces = Interfaces.objects.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_interfaces,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        interfaces = p.page(page)
        return render(request,"interfaceManage.html",{"interfaces":interfaces})


#查询接口管理数据
class SearchIntfView(View):
    def get(self,request,sprj,smod):
        #查询全部数据
        if sprj =="null" and (smod=="null" or smod==None) :
            all_interfaces = Interfaces.objects.all()
        #查询项目下的接口
        elif sprj !="null" and smod=="null":
            all_interfaces = Interfaces.objects.filter(projectId__project_name=sprj)
        #查询模块下的接口
        elif sprj !="null" and smod !="null":
            all_interfaces = Interfaces.objects.filter(projectId__project_name=sprj,projectId__module_name=smod )

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_interfaces,5, request=request) #第一个参数是待分页的数据，第二个参数是每页显示多少数据
        interfaces = p.page(page)
        return render(request,"interfaceManage.html",{"interfaces":interfaces})

#登录
class LoginView(View):
    def get(self,request):
        #如果用户已登录，直接跳转到base页面
        if request.user.is_authenticated():
            return render(request,'base.html')
        else:
            return render(request,'login.html')
    def post(self,request):
        user_name = request.POST.get("username","")
        pass_word = request.POST.get("password","")
        user = authenticate(username=user_name,password=pass_word)
        #如果返回user对象说明用户名和密码正确，则调用login方法进行登录;不正确则停留在登录页面
        if user is not None:
            login(request,user)
            return render(request,"base.html")
        else:
            return render(request,"login.html",{"message":"用户名或密码错误"})

#退出登录
class LogoutView(View):
    def get(self,request):
        auth.logout(request)
        return render(request,'login.html')

















