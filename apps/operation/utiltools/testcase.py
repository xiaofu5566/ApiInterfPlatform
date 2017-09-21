#-*- coding:utf-8 -*-
__author__ = 'furong'
__date__ = '2017/8/5 16:30'
import requests
import json


class Webrequests:
    def get(self,url,para,headers):
        try:
            r = requests.get(url,params=para,headers=headers)

        except BaseException as e:
            r = "get方法出错，请检查头信息和参数是否正确"

        return r

    def post_json(self,url,para,headers):
        try:
            data = para
            #data = json.dumps(data)   #python数据类型转化为json数据类型
            r = requests.post(url,data=data,headers=eval(headers))
        except BaseException as e:
            r="post方法出错，请检查头信息和参数是否正确"

        return r



