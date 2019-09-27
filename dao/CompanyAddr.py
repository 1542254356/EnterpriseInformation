from dao.MySQLBase import MySQLBase


class CompanyAddr(MySQLBase):
    def __init__(self):
        super().__init__()
        self.table = 't_company_addr'

    '''
    读取数据库为字典
    '''
    def getDic(self):
        sql = 'SELECT * FROM %s'% (self.table)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            dic = {}
            for row in results:
                company = row[1]
                addr = row[2]
                dic[company] = addr
            return dic
        except Exception as e:
            print(e)
            return None

    def saveDic(self,dic):
        try:
            for kv in dic.items():
                company = kv[0]
                addr = kv[1]
                sql = 'REPLACE INTO %s(cname, addr) VALUES ("%s","%s");' % (self.table, company, addr)
                self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)
            return None



if __name__ == '__main__':
    compantAddr = CompanyAddr()
    # dic = compantAddr.getDic()
    # print(dic)
    dic = {'公司1': '地址111', 'gs': 'dzdz'}
    compantAddr.saveDic(dic)

