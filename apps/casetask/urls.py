#-*- coding:utf-8 -*-
__author__ = 'furong'
__date__ = '2017/8/12 12:00'
from django.conf.urls import url
from .views import CaseTaskListView,AddTskView,InitTaskView,AlterTaskView,DeleTaskView,SearchTaskView,RsReportListView,DeleReportView,SearchReptView,InitDataView
urlpatterns = [
    url(r'^showtasks/',CaseTaskListView.as_view(),name="showtasks"),
    url(r'^addtask/',AddTskView.as_view(),name="addtask"),
    url(r'^inittask/',InitTaskView.as_view(),name="inittask"),
    url(r'^altask/',AlterTaskView.as_view(),name="altask"),
    url(r'^del_task/(?P<taskid>.*)/$',DeleTaskView.as_view(),name="del_task"),
    url(r'^searchTask/(?P<taskname>.*)/$',SearchTaskView.as_view(),name="searchTask"),
    url(r'^rsreportlist/',RsReportListView.as_view(),name="rsreportlist"),
    url(r'^del_report/(?P<repid>.*)/$',DeleReportView.as_view(),name="del_report"),
    url(r'^searchRp/(?P<taskname>.*)/$',SearchReptView.as_view(),name="searchRp"),
    url(r'^initdata/',InitDataView.as_view(),name="initdata"),
]