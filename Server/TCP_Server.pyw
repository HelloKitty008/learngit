#-*- coding: utf-8-*-
from socket import *
import threading
import string
import sys
from DB import *
from picture_write import *
import json
import time

#异常照片
pic=Picture_write()
#数据库对象
db=DB()
#客户端队列
client_list=[]



#数据库线程
def DB_thread(PLSNO,ActNum,SESign,BreakSign,BreakIma,DateTime):
    db.ExecUpdata(PLSNO,ActNum,SESign,BreakSign,BreakIma,DateTime)
    
    #服务端
def Socket_thread(conn,addr):
    clientname='client'+'%s'%(addr[0])
    clientname=conn
    db.Monitor(addr[0],1)#在线
    client_list.append(clientname)
    sign=0
    Thread_sign=True
    buf=''
    buf1=''
    while Thread_sign:
        try:
            buf=str(conn.recv(1024),"utf-8")
        except:
            sign=1
            conn.close()
            db.Monitor(addr[0],0)#掉线
            client_list.remove(clientname)
            #结束线程
            Thread_sign=False
        if not len(buf):
            break
        if sign==0 and buf!=buf1 and buf != '0000':
            buf1=buf
            print(buf)
            try:
            #解析json
                Rec_data=json.loads(buf)
                PLSNO = Rec_data["PLSNO"]
                ActNum = Rec_data["ActNum"]
                SESign = Rec_data["SESign"]
                BreakSign = Rec_data["BreakSign"]
                BreakIma = Rec_data["BreakIma"]
                DateTime = Rec_data["DateTime"]
                t=threading.Thread(target=DB_thread,args=(PLSNO,ActNum,SESign,BreakSign,BreakIma,DateTime))
                t.start()
            except:
                pass
    conn.close()
    #发送订单
def sendplsno(HOST,PLSNO):
    port=12310
    s=socket(AF_INET,SOCK_DGRAM)
    s.connect((HOST,port))
    s.sendall(bytes(PLSNO,encoding="utf-8"))
    
  #生产信息接收
def TCP_server(port):
    #创建TCP套接字
    sock=socket(AF_INET,SOCK_STREAM)
    #绑定地址和端口
    s_addr=("0.0.0.0",port)
    sock.bind(s_addr)
    #侦听客户端
    sock.listen(50)
    while True:
        time.sleep(0.01)
        conn,addr=sock.accept()
        t=threading.Thread(target=Socket_thread,args=(conn,addr))
        t.start()
        print(addr)
#计划单号接收
def Plsno():
    sock_plson=socket(AF_INET,SOCK_STREAM)
    ADDR=("0.0.0.0",19800)
    sock_plson.bind(ADDR)
    sock_plson.listen(3)
    while True:

        conn,addr=sock_plson.accept()
        while True:
            try:
                buf=str(conn.recv(1024),encoding="utf-8")
            except:
                conn.close()
                break
            if not len(buf):
                break
            Rec_data=json.loads(buf)
            Type=Rec_data["Type"]
            PLSNO=Rec_data["PLSNO"]
            DnsIP=Rec_data["DnsIP"]
            PortNumber=Rec_data["PortNumber"]
            #发送
            if Type=='s':
                S1=sendplsno(DnsIP,PLSNO)
                conn.sendall(bytes('True',encoding="utf-8"))
            #回撤
            if Type=='r':
                pass
if __name__ == "__main__":
    try:
        #计划单号
        t=threading.Thread(target=Plsno,args=())
        t.start()
        time.sleep(1)
        #故障图片
        t=threading.Thread(target=pic.Listen,args=())
        t.start()
        time.sleep(1)
        #写数据线程
        t=threading.Thread(target=db.Q_sql,args=())
        t.start()
        time.sleep(1)
        TCP_server(12315)
    except:
        pass
