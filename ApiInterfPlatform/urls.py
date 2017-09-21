#-*- coding:utf-8 -*-
"""ApiInterfPlatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.views.generic import TemplateView
from django.conf.urls import url,include
from django.contrib import admin

from interfcacePlat.views import BaseView, ProjListView,SearcView,InterfListView,ModListView,AddInterView,AlterInterfaceView,ShowInterfView,\
    Del_IntefView,SearchIntfView,LoginView,LogoutView,AddPrjView,AlterPrjView,DelPrjView,ShowPrjView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #登录
    url(r'^login/$',LoginView.as_view(),name="login"),
    #退出登录
    url(r'^logout/$',LogoutView.as_view(),name="logout"),

    url(r'^index/',BaseView.as_view(),name="index"),
    #项目模块列表
    url(r'^proj/$',ProjListView.as_view(),name="proj"),
    #项目模块增加
    url(r'^addproj/$',AddPrjView.as_view(),name="addproj"),
    #项目模块修改
    url(r'^alproj/$',AlterPrjView.as_view(),name="alproj"),

    url(r'^showprj/$',ShowPrjView.as_view(),name="showprj"),


    url(r'^delprj/(?P<prjid>.*)/$',DelPrjView.as_view(),name="delprj"),

    url(r'^srcprj/(?P<prj>.*)/(?P<mod>.*)/$',SearcView.as_view(),name="srcprj"),
    #接口管理
    url(r'^intflist/',InterfListView.as_view(),name="intflist"),
    url(r'^searchmods/',ModListView.as_view(),name="searchmods"),
    url(r'^addinterface/',AddInterView.as_view(),name="addinterface"),
    url(r'^alterinterface/',AlterInterfaceView.as_view(),name="alterinterface"),
    url(r'^showInterf/',ShowInterfView.as_view(),name="showInterf"),
    url(r'^del_intf/(?P<delid>.*)/$',Del_IntefView.as_view(),name="del_intf"),
    url(r'^searchInf/(?P<sprj>.*)/(?P<smod>.*)/$',SearchIntfView.as_view(),name="searchInf"),

    #接口用例urls配置
    url(r'^cases/',include('casesPlat.urls',namespace="cases")),

    #执行接口用例urls配置
    url(r'^testc/',include('operation.urls',namespace="testc")),

    #测试任务urls配置
    url(r'^taskc/',include('casetask.urls',namespace="taskc")),


]
