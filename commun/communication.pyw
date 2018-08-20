#-*- coding: utf-8-*-
import socket
from MYSQL import *
import datetime
import threading
import time
import queue

#import ctypes12
class communication():
    def __init__(self,):
        self.conn=False
        self.DB=MYSQL(host='127.0.0.1',user="root",pwd="1234",db="zhusuji")
    #插入新订单
    def INSERT_NEW_PLSON(self,PLSNO):
        try:
            PLSON=PLSNO
            INSERT_TIME = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            PROCESS = 'process'+PLSNO
            REGION = 'region_'+PLSNO
            INFO = 'info_'+PLSNO
            #插入订单号
            STRSQL_INSERT_PLSON="insert into ALL_PLSNO(PLSNO,getfrom,writetime,lasttime,process_table,region_table,info_table) values('%s','NET','%s','%s','%s','%s','%s')"%(PLSON,INSERT_TIME,INSERT_TIME,PROCESS,REGION,INFO)
            self.DB.ExecNonQuery(STRSQL_INSERT_PLSON)
        except:
            return 0
        return 1
        '''
        #创建表：region_+计划编号
        STRSQL_CREATE_REGION=" CREATE TABLE %s(id int(4) primary key not null auto_increment,regionnum text,leftx text,lefty text,rightx text,righty text,leftT text,leftB text,rightT text,rightB text,thre text,sub_thre text,sub_scale text,cameraid text,testorder text)character set = utf8"%(REGION)
        DB.ExecNonQuery(STRSQL_CREATE_REGION)
        for number in range(0,100):
            
            STRSQL_INSERT_TEGION="insert into %s(regionnum,thre,testorder) values(%s,'0.5','0');"%(REGION,number)#insert 100次（i对应次数）
            DB.ExecNonQuery(STRSQL_INSERT_TEGION)
        #创建表info_+计划编号
        STRSQL_CREATE_INFO="create table %s(id int(4) primary key not null auto_increment,first_usable text,needle_times text,delay1 text,delay2 text,second_times text,second_space text,push_times text) character set = utf8"%(INFO)
        DB.ExecNonQuery(STRSQL_CREATE_INFO)
        STRSQL_INSERT_INFO="insert into %s(first_usable,needle_times,delay1,delay2,second_times,second_space,push_times) values('1','1','0','0','0','0','0')"%(INFO)
        DB.ExecNonQuery(STRSQL_INSERT_INFO)

        '''
    #读取数据库
    def READ_DB(self,):
        '''
        元组下标：
        [0]: ID表ID
        [1]：PLSNO计划号
        [2]：ActNum当前生产总数
        [3]：SESign生产标识(0为开始生产，1为生产中，2为生产结束)
        [4]：BreakSign故障标识(0为正常，1为故障)
        [6]: DateTime记录时间
        [7]: IsSend 本条记录是否已经发送，未发送时为None
        '''
        while True:
            #STRSQL="select * from process where IsSend is null"
            STRSQL="select * from process"
            db=self.DB.ExecQuery(STRSQL)
            if db:
                tuplelen=len(db)#元组长度
                for number in range(0,tuplelen):
                    ID = db[number][0]
                    PLSNO = db[number][1]
                    ActNum = db[number][2]
                    SESign = db[number][3]
                    BreakSign = db[number][4]
                    BreaIma = db[number][5]
                    DateTime = db[number][6]
                    time.sleep(0.1)
                    '''
                    if BreaIma!=None:
                        t=threading.Thread(target=self.Picture_transmis,args=(PLSNO,BreaIma))
                        t.start()
                    '''
                    if self.conn:
                        s20='{"PLSNO":"%s","ActNum":"%s","SESign":"%s","BreakSign":"%s","BreakIma":"%s","DateTime":"%s"}'%(PLSNO,ActNum,SESign,BreakSign,BreaIma,DateTime)
                        try:   
                            self.conn.sendall(bytes(s20,encoding="utf-8"))
                            PROCESS_DELETE="DELETE FROM process where ID=%s"%(ID)
                            self.DB.ExecNonQuery(PROCESS_DELETE)
                        except:
                            self.conn=False

    #传递错误图片
    def Picture_transmis(self,PLSNO,Picture):
        Picture_Path="D:/模具保护/Application/save/%s/error_image/%s"%(PLSNO,Picture)
        conn=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            conn.connect(('192.168.0.47',8001))
            conn.sendall(bytes(Picture,encoding="utf-8"))
            s=conn.recv(1024)
            if s:
                with open(Picture_Path,'rb') as f:
                    while True:
                        data=f.read(2048)
                        if not data:
                            break
                            f.close()
                        conn.sendall(data)
        except:
            pass
    def comm(self):
        while True:
            time.sleep(1)
            if self.conn==False:
                #print('conn.....')
                time.sleep(1)
                try:
                    self.conn=socket.socket()
                    self.conn.connect(("192.168.0.47",12315))
                except:
                    self.conn=False
    #计划           
    def plsno(self):
        host=''
        port=12310
        addr =(host,port)
        udpserver=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        udpserver.bind(addr)
        while True:
            data,addr=udpserver.recvfrom(1024)
            plsno=str(data,encoding="utf-8")
            a=self.INSERT_NEW_PLSON(plsno)
            #print(a)
            '''
            if a==1:
                udpserver.sendto(bytes('1',encoding="utf-8"),addr)
                
            '''
    def test(self):
        while True:
            time.sleep(30)
            try:
                teststr = '0000'
                self.conn.sendall(bytes(teststr,encoding="utf-8"))
            except:
                self.conn = False
            
        
                
c=communication()

t=threading.Thread(target=c.comm,args=())
t.start()

t=threading.Thread(target=c.plsno,args=())
t.start()

t=threading.Thread(target=c.test,args=())
t.start()


c.READ_DB()

