#-*- coding: utf-8-*-
from MSSQL import *
import datetime
import time
import queue


class DB:

    def __init__(self,):
        #消息队列
        self.q=queue.Queue()
        
        #数据库服务器配置
        self.host ="192.168.0.47:1433"
        self.user="sa"
        self.password="server"
        self.database="SEWeb"
        self.ms=MSSQL(host=self.host,user=self.user,pwd=self.password,db=self.database)
        #在线状态检测
    def Monitor(self,ip,status):
        s="exec [dbo].UpdateKJ_SmartEye_Monitor '9','%s','8000','%s'"%(ip,status)
        self.q.put(s)
        '''
        #print(s)
        try:
            self.ms.ExecNonQuery(s)
            time.sleep(1)
        except:
            try:
                self.ms.ExecNonQuery(s)
                time.sleep(1)
            except:
                pass
        '''
    def ExecUpdata(self,PLSNO,ActNum,SESign,BreakSign,BreakIma,DateTime):
        time.sleep(0.01)
        self.PLSNO=PLSNO
        self.ActNum=ActNum
        self.SESign=SESign
        self.BreakSign=BreakSign
        self.BreakIma=BreakIma
        self.WriteTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.da_time = DateTime
        if self.BreakIma=='null':
            self.BreakIma=''
        s1="exec [dbo].[InsertKJ_SmartEye_Actual] '%s','%s','%s','%s','%s','%s'"%(self.PLSNO,ActNum,SESign,self.BreakSign,self.BreakIma,self.da_time)
        self.q.put(s1)
        '''
        #test code
        Time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       
        #self.ms.ExecNonQuery("exec [dbo].[InsertKJ_SmartEye_Actual] 'PL180100000003','1','2','0','','%s'"%(Time))
        
        try:
            self.ms.ExecNonQuery("exec [dbo].[InsertKJ_SmartEye_Actual] '%s','%s','%s','%s','%s','%s'"%(self.PLSNO,ActNum,SESign,self.BreakSign,self.BreakIma,self.WriteTime))
            #print(self.PLSNO,ActNum,SESign,self.BreakSign,self.BreakIma,self.WriteTime)
        except:
            try:
                time.sleep(1)
                self.ms.ExecNonQuery("exec [dbo].[InsertKJ_SmartEye_Actual] '%s','%s','%s','%s','%s','%s'"%(self.PLSNO,ActNum,SESign,self.BreakSign,self.BreakIma,self.WriteTime))
            except:
                try:
                    time.sleep(1)
                    self.ms.ExecNonQuery("exec [dbo].[InsertKJ_SmartEye_Actual] '%s','%s','%s','%s','%s','%s'"%(self.PLSNO,ActNum,SESign,self.BreakSign,self.BreakIma,self.WriteTime))
                except:
                    pass
                    #print('sql error')
        '''
    def Q_sql(self,):
        while True:
            #print(self.q.qsize())
            try:
                strsql=self.q.get()
            except:
                pass
            try:
                self.ms.ExecNonQuery(strsql)
            except:
                try:
                    self.ms.ExecNonQuery(strsql)
                except:
                    pass
                
            
        



        
        
