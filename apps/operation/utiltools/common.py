#-*- coding:utf-8 -*-
__author__ = 'furong'
__date__ = '2017/9/4 14:59'
import json

#将/uxxx/uxxxx 数据转化为中文
def to_chinese(unicode_str):
    x = json.loads('{"chinese":"%s"}' % unicode_str)
    return x['chinese']

test = to_chinese([u'\u75bc\u75db',u'\u75bc\u75db'])
print test

