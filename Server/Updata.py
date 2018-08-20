#-*- coding: utf-8-*-
from MSSQL import *
import datetime
import time


class Updata:

    def __init__(self,PLSNO,ActNum,SESign,BreakSign,BreakTma,WriteTime):

        self.PLSNO=PLSNO
        self.ActNum=ActNum
        self.SESign=SESign
        self.BreakSign=BreakSign
        self.BreakTma=BreakTma
        self.WriteTime=WriteTime

    def ExecUpata():

        #数据库服务器配置
        host ="192.168.0.47:1433"
        user="sa"
        password="server"
        database="SEWeb"
        ms=MSSQL(host=host,user=user,pwd=password,db=database)
        #Time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ms.ExecNonQuery("exec [dbo].[InsertKJ_SmartEye_Actual] '%s','%s',%s'','%s','%s','%s'"% (self.PLSNO,self.ActNum,self.SESign,self.BreakSign,self.BreakTma,WriteTime))
