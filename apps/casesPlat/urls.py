#-*- coding:utf-8 -*-
__author__ = 'furong'
__date__ = '2017/8/2 11:10'
from django.conf.urls import url,include

from .views import CasesListView,AddCasesView,SearchUriView,SearchMhpView,InitCasesView,AlterCaseView,SearchCasesView,Del_caseView
urlpatterns = [
    url(r'^showCases/',CasesListView.as_view(),name="intfcaselist"),
    url(r'^addcases/',AddCasesView.as_view(),name="addcases"),
    url(r'^searchuri/',SearchUriView.as_view(),name="searchuri"),
    url(r'^searchmhp/',SearchMhpView.as_view(),name="searchmhp"),
    url(r'^showInterfcase/',InitCasesView.as_view(),name="showInterfcase"),
    url(r'^altercase/',AlterCaseView.as_view(),name="altercase"),
    url(r'^searchCases/(?P<sprj>.*)/(?P<smod>.*)/(?P<casepath>.*)/$',SearchCasesView.as_view(),name="searchCases"),
    url(r'^del_case/(?P<caseid>.*)/$',Del_caseView.as_view(),name="del_case"),

]

