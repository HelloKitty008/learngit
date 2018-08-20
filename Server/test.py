from MSSQL import *


ms=MSSQL("192.168.0.47","sa","server","SEWeb")

ms.ExecNonQuery("exec [dbo].UpdateKJ_SmartEye_Monitor'9','192.168.0.213','8000','1'")
