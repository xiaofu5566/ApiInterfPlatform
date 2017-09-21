#-*- coding:utf-8 -*-
__author__ = 'furong'
__date__ = '2017/9/6 16:08'
import MySQLdb
#执行sql语句并关闭连接
def dbexc(db,cursor,sql):
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
        # 关闭数据库连接
    db.close()

#初始化库存/积分
def InitScOrSt(envir,type,data):
    if envir=="测试环境" and type=="积分":
        # 打开数据库连接
        db = MySQLdb.connect("192.168.16.33","root","WoChu@123","wicplatform" )
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        sql = "update memberaccount set score='%d' where memberid in (select id from member where account in('15556925769'))"%(data)
        dbexc(db,cursor,sql)

    elif envir=="测试环境" and type=="库存":
        # 打开数据库连接
        db = MySQLdb.connect("192.168.16.33","root","WoChu@123","onlinestock" )
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        sql = "update online_stock set stock_saleble='%d'"%(data)
        dbexc(db,cursor,sql)

    elif envir=="预生产环境" and type=="积分":
        # 打开数据库连接
        db = MySQLdb.connect("114.55.190.10","ysctester","ZhSuxJu8y-un5","wicplatform" )
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        sql = "update memberaccount set score='%d' where memberid in (select id from member where account in('15556925769'))"%(data)
        dbexc(db,cursor,sql)

    elif envir=="预生产环境" and type=="库存":
        # 打开数据库连接
        db = MySQLdb.connect("114.55.190.10","ysctester","ZhSuxJu8y-un5","onlinestock" )
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        sql = "update online_stock set stock_saleble='%d'"%(data)
        dbexc(db,cursor,sql)





