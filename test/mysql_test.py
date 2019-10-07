from mysqldb import Database
import os
import sys
sys.path.append(os.path.abspath('..'))
from excel.readExistInfo import get_corp_addr_map_and_names

if __name__ == '__main__':
    with Database(tb_name='table_test') as db:
        assert hasattr(db, 'connected'), '数据库连接失败'
        # corp_addr, corp = get_corp_addr_map_and_names(
        #     os.path.join('sh.xls' )
        # )
        # db.write_many(
        #     [
        #         {
        #             'id': i,
        #             'cname': e[0],
        #             'addr': e[1]
        #         }
        #         for i, e in enumerate(corp_addr.items())
        #     ]
        # )
        
        # for k, v in corp_addr.items():
        #     print(k, v)
        #     try:
        #         db.write(i, k, v)
        #     except Exception as e:
        #         print(e)
        #         with open('err.log', 'a') as f:
        #             print(f'error occured: NO.{i}, {k}, {v}', file=f)
        #     i += 1
        # 注意不要重复写入
        # try:
        #     db.write(123, 'test', 'XC')
        # except Exception:
        #     print('检查是否重复写入？')
        rst = db.raw_query(f'select * from {db.table_name}')
        # # 请求结果导出字典
        # print(rst.as_dict())
        # # 导出excel
        db.rst_export_as(rst, 'xls', 'test2.xls')
