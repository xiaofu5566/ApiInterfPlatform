#-*- coding:utf-8 -*-
__author__ = 'furong'
__date__ = '2017/7/6 11:02'
from django import forms

class ProjForm(forms.Form):
    project_name = forms.CharField(max_length=10,required=True)
    module_name = forms.CharField(max_length=10,required=True)

