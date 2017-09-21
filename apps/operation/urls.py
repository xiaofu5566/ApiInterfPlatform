#-*- coding:utf-8 -*-
__author__ = 'furong'
__date__ = '2017/8/2 11:10'
from django.conf.urls import url,include

from .views import SingleCaseView,TestCaseView,SaveCaseView,ManyCaseTestsView,ReportDetailView,CopyAllView

urlpatterns = [
    url(r'^singlecase/(?P<intfid>.*)/$',SingleCaseView.as_view(),name="singlecase"),
    url(r'^testcase/$',TestCaseView.as_view(),name="testcase"),
    url(r'^savecase/$',SaveCaseView.as_view(),name="savecase"),
    url(r'^manycasetest/$',ManyCaseTestsView.as_view(),name="manycasetest"),
    url(r'^detail/(?P<id>.*)/(?P<flag>.*)',ReportDetailView.as_view(),name="detail"),
    url(r'^copyall/$',CopyAllView.as_view(),name="copyall"),
]

