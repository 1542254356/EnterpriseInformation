import pymysql


class MySQLBase:
    def __init__(self):
        self.host = 'i.hjwblog.com'
        self.user = 'enterprise'
        self.passwd = 'enterprise123'
        self.dbName = 'db_enterprise'
        # 打开数据库连接
        self.db = pymysql.connect(self.host, self.user, self.passwd, self.dbName)
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()




    def close(self):
        self.db.close()

if __name__ == '__main__':
    mysql = MySQLBase()
