#-*- coding:utf-8 -*-
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render
from django.views.generic.base import View
from datetime import datetime
from django.http import HttpResponse
import json
import pyperclip

from interfcacePlat.models import Interfaces
from casesPlat.models import InterCases
from casetask.models import CaseTask,CaseResults,ResultReport
from interfcacePlat.models import Interfaces,Projects
from utiltools.testcase import Webrequests


import sys
import uuid
import unittest

reload(sys)

sys.setdefaultencoding('utf8')
# Create your views here.
#初始化单个接口测试页面数据
class SingleCaseView(View):
    def get(self,request,intfid):
        interface = Interfaces.objects.get(id=intfid)
        method = interface.interf_method
        uri = interface.interf_url
        headinf = interface.interf_header
        parms = interface.interf_param
        return render(request,'singleCaseExc.html',{"method":method,"uri":uri,"headinf":headinf,"parms":parms,"intfid":intfid})

#执行单个测试用例
class TestCaseView(View):
    def post(self,request):
        ip = request.POST.get("ip")
        uri = request.POST.get("uri")
        headinf = request.POST.get("headinf")
        parm = request.POST.get("parm")
        method = request.POST.get("method")

        #rs = TestSingleCase().testsinglecase(ip,uri,method,parm,headinf)
        #content = {"rs":rs}
        re = Webrequests()
        url = "http://"+ip+uri
        if method=="get":
            rs = re.get(url,parm,headinf)
        elif method=="post":
            rs = re.post_json(url,parm,headinf)
        content = {"rs":rs.text,"restatu":rs.status_code}
        return HttpResponse(json.dumps(content))

#将单个接口测试的数据保存为测试用例
class SaveCaseView(View):
    def post(self,request):
        uri = request.POST.get("uri")
        headinf = request.POST.get("headinf")
        parm = request.POST.get("parm")
        method = request.POST.get("method")
        casename = request.POST.get("casename")
        expectrst = request.POST.getlist("expectrst")

        exrsnums = len(expectrst)
        expectRs_save = ""
        #用字符串的方式存储预期结果，用分号分割多个预期结果
        for i in range(len(expectrst)):
            if i<len(expectrst)-1:
                expectRs_save = expectRs_save+expectrst[i]+";"
            elif i==len(expectrst)-1:
                expectRs_save = expectRs_save+expectrst[i]
        intf_id = request.POST.get("intf_id")

        case = InterCases()
        case.casename = casename
        case.expectRs = expectRs_save
        case.headinfo = headinf
        case.interid_id = intf_id
        case.param = parm
        case.expectRs_nums = exrsnums
        case.save()
        return render(request,'singleCaseExc.html',{"method":method,"uri":uri,"headinf":headinf,"parms":parm,"intfid":intf_id})

#批量执行接口测试用例
class ManyCaseTestsView(View):
    #批量执行接口用例
    def casestest(self,method,url,parm,headinf,expectRs):
        re = Webrequests()
        if method=="get":
            rs = re.get(url,parm,headinf)
            rstext = rs.text

            #遍历预期结果，如果实际结果包含所有的预期结果，则用例执行成功
            istrue = 1
            for exrs in expectRs:
                if rstext.find(exrs)!=-1:
                    istrue = (istrue)& 1
                else:
                    istrue = (istrue)& 0
            return istrue,rstext
        elif method=="post":
            rs = re.post_json(url,parm,headinf)
            rstext = rs.text
            #如果实际结果包含预期结果，则用例执行成功
            if rstext.find(expectRs):
                istrue = 0
            else:
                istrue = 1
            return istrue,rstext

    #执行测试并保存结果到结果集,返回这一批次的flag
    def loopcase(self,cases,taskip,taskid):

        #给每次执行测试任务的时候产生一个唯一的标识，便于后面生成测试报告
        flag = uuid.uuid4()
        for mycase in cases:
            uri = Interfaces.objects.get(id=mycase.interid_id).interf_url
            headinf = mycase.headinfo
            parm = mycase.param
            method = Interfaces.objects.get(id=mycase.interid_id).interf_method
            expectRs = mycase.expectRs
            expectRs_list = expectRs.split(";")
            url = "http://"+taskip+uri

            #批量测试接口用例
            manycasers = ManyCaseTestsView().casestest(method,url,parm,headinf,expectRs_list)

            #将执行结果存入结果集表
            casers = CaseResults()
            casers.taskid = taskid
            casers.caseid = mycase
            casers.realresult = manycasers[1]
            casers.istrue = manycasers[0]
            casers.updatetime = datetime.now()
            casers.flag = flag

            casers.save()
        return flag

    #记录数据进入测试报告表
    def saveReport(self,taskid,durtime,flag):
        cr = CaseResults.objects.filter(taskid=taskid).filter(flag=flag) #查询某任务对应的结果集
        crfail = CaseResults.objects.filter(taskid=taskid).filter(flag=flag).filter(istrue=1) #查询某任务中失败结果集
        cr_failnums= len(crfail) #计算失败数
        cr_nums = len(cr) #计算某任务总的结果数

        taskname = CaseTask.objects.get(id=taskid).task_name
        rsp = ResultReport()
        rsp.name =taskname+datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        rsp.taskid_id = taskid
        rsp.durt = durtime
        rsp.failnum = cr_failnums
        rsp.nums = cr_nums
        rsp.flag = flag
        rsp.creattime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        rsp.save()


    def get(self,request):
        taskid = request.GET.get("taskid")
        taskip = request.GET.get("taskip")
        casetask = CaseTask.objects.get(id=int(taskid))
        exec_plan = casetask.exec_plan

        if exec_plan==u"项目名":
            #根据执行计划，查出项目名称
            prjname = casetask.prj_name
            #根据该项目下所有接口
            interface = Interfaces.objects.filter(projectId__project_name=prjname)
            #创建一个空的intercases queryset对象
            cases = InterCases.objects.none()
            #遍历接口，查询每个接口对应的接口用例，并合并成一个queryset
            for i in interface:
                case = InterCases.objects.filter(interid_id=i.id)
                cases = cases|case
            #记录测试开始时间
            time1 = datetime.now()
            flag = ManyCaseTestsView().loopcase(cases,taskip,taskid)
            #记录测试结束时间
            time2 =datetime.now()
            #计算测试耗时
            durtime = (time2-time1).microseconds

           #保存测试报告数据
            ManyCaseTestsView().saveReport(taskid,durtime,flag)
            content = {"message":"执行完毕"}
            return HttpResponse(json.dumps(content))

        elif exec_plan==u"用例id":
            caseids = casetask.case_id
            case_id_list = caseids.split(",")
            #创建一个空的intercases queryset对象
            cases = InterCases.objects.none()
            #遍历接口，查询每个接口对应的接口用例，并合并成一个queryset
            for id in case_id_list:
                case = InterCases.objects.filter(id=id)
                cases = cases|case

            #记录测试开始时间,取毫秒
            time1 = datetime.now().microsecond

            flag =  ManyCaseTestsView().loopcase(cases,taskip,taskid)

            content = {"message":"执行完毕"}

            #记录测试结束时间
            time2 =datetime.now().microsecond
            #计算测试耗时,取毫秒
            durtime = time2-time1

            #保存测试报告数据
            ManyCaseTestsView().saveReport(taskid,durtime,flag)

            return HttpResponse(json.dumps(content))

#查看报告详情
class ReportDetailView(View):
    def get(self,request,id,flag):
        #查询报告相关字段
        rr = ResultReport.objects.get(id=id)
        taskid = rr.taskid_id
        nums = rr.nums
        failnum = rr.failnum
        succnum = nums-failnum #计算测试通过用例数

        #查询报告关联的结果集数据
        crs = CaseResults.objects.filter(taskid=taskid,flag=flag)
        return render(request,'resultDetail.html',{'casereslt':crs,'casereport':rr,'succnum':succnum})

#一键复制
class CopyAllView(View):
    def post(self,request):
        ip = request.POST.get("ip")
        uri = request.POST.get("uri")
        headinf = request.POST.get("headinf")
        parm = request.POST.get("parm")
        method = request.POST.get("method")
        restat = request.POST.get("restat")
        retext = request.POST.get("retext")

        #根据不同方法拼接要复制粘贴的数据
        if method=="get":
            str_all = ip+uri+parm+"  "+method+"\r\n"+headinf+"\r\n"+"响应状态码："+restat+"\r\n"+"响应主体："+retext
        elif method == "post":
            str_all = ip+uri+"  "+method+"\r\n"+headinf+"\r\n"+parm+"\r\n"+"响应状态码："+restat+"\r\n"+"响应主体："+"\r\n"+retext
        #复制
        pyperclip.copy(str_all)

        content = {"message":"已复制成功，可在任意文本工具中粘贴该数据"}

        return HttpResponse(json.dumps(content))



















