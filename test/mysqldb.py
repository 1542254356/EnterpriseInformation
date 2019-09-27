import records


class Database:
    '''数据库读写封装类'''
    def __init__(self):
        '''使用records库操作MySQL，还是面向对象的方式舒服一点'''
        n = 0
        while n < 3:
            try:
                db = records.Database('mysql://enterprise:enterprise123@hjwblog.com/db_enterprise')
                break
            except ModuleNotFoundError:
                # 第一次运行可能会报错，需要执行一次即可
                import pymysql
                pymysql.install_as_MySQLdb()
        self.db = db
        
    def write(self, id, corp_name, addr):
        '''写入数据库'''
        self.db.query(f'insert into t_company_addr values({id},"{corp_name}", "{addr}")')
        
    def query_as_dict(self, sql):
        '''将请求的结果按照字典返回'''
        rows = self.db.query(sql)
        return rows.as_dict()
    
    def raw_query(self, sql):
        '''使用records的SQL接口'''
        return self.db.query(sql)
    
    def rst_export_as(self, rst, export_t, fn=''):
        '''将请求的结果按照一定格式导出
        
        rst: raw_query请求的结果
        export_t: 导出类型，支持xls, json, yaml, csv
        fn: 导出文件名，可选参数，导出文件必须'''
        if export_t == 'xls':
            with open(fn, 'wb') as f:
                f.write(rst.export('xls'))
            print('写入xls文件成功')
        elif export_t in ['json', 'yaml', 'csv']:
            return rst.export(export_t)
        else:
            print('不支持的导出类型')
                    
    def close(self):
        self.db.close()
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()