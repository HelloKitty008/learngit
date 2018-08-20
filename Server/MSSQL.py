import pymssql

class MSSQL(object):
    """
      pymssql 模块封装
    """
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
    def __GetConnect(self):
        """
         连接数据库
         """
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "数据库连接失败")
        else:
            return cur

    def ExecQuery(self, sql):
        """
        执行查询

        返回的是一个包含tuple的list,list的元素是记录行，tuple的元素是每行记录的字段
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        # 查询结束关闭连接
        self.conn.close()
        return resList

    def ExecNonQuery(self, sql):
        """
         执行非查询语句
         """
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()
