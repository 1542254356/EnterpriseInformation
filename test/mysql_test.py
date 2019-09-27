from mysqldb import Database
        
        
if __name__ == '__main__':
    with Database() as db:
        print('数据库连接成功')
        # 注意不要重复写入
        try:
            db.write(123, 'test', 'XC')
        except Exception:
            print('检查是否重复写入？')
        rst = db.raw_query('select * from t_company_addr')
        # 请求结果导出字典
        print(rst.as_dict())
        # 导出excel
        db.rst_export_as(rst, 'xls', 'test2.xls')
