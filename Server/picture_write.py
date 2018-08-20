# -*- coding: utf-8 -*-
from socket import *
import os
import threading
class Picture_write(object):
    def __init__(self):
        self.HOST = ''
        self.PORT = 8001
        self.BUFSIZ = 1024
        self.ADDR = (self.HOST, self.PORT)
        __PathName = 'd:\\智能视觉监控系统\\SEManage\\Files'
        if os.path.exists(__PathName):
            os.chdir(__PathName)
        else:
            os.makedirs(__PathName)
            os.chdir(__PathName)
    def Thread_Picture(self,conn,addr):
        try:
            pic_name=conn.recv(1024)
            print(pic_name)
            conn.sendall(bytes('ok',encoding="utf-8"))
            if pic_name:
                with open(pic_name,'wb')as f:
                    while True:
                        buf= conn.recv(2048)
                        if not buf:
                            break
                        f.write(buf)
                    f.close()
        except:
            pass
                    
    def Listen(self):
        #print('wait for pic')
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind(self.ADDR)
        sock.listen(50)
        while True:
            conn, addr = sock.accept()
            t = threading.Thread(target=self.Thread_Picture, args=(conn, addr))
            t.start()

