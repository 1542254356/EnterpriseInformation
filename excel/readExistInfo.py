# 读取excel文件里面已有的公司名字和地址映射

import xlrd
import xlwt
import random
import re
from xlutils.copy import copy


class Excel2Dict:
    def __init__(self, xls='test/sh.xls', sheet_index=0):
        '''将excel转换成dict的类
        
        xls: 打开的excel文件名
        sheet_index: 第几张表'''
        book = xlrd.open_workbook(xls)
        self.fn = xls
        self.sheet = book.sheet_by_index(0)
        self.title = [_.value for _ in self.sheet.row(0)]
        self.row_num = self.sheet.nrows
        headers = [v.value for v in self.sheet.row(0)]
        for i, e in enumerate(headers):
            if e == '申请人':
                self.cname_col = i
            elif e == '申请人地址':
                self.addr_col = i
            elif e == '申请人类型':
                self.type_col = i

    def get_dict_by_row(self, row):
        '''传入行号，返回字典'''
        r = self.sheet.row(row)
        try:
            rst_dict = {
                'cname': r[self.cname_col].value,
                'addr' : r[self.addr_col].value,
                'type' : r[self.type_col].value
            }
        except KeyError:
            print(f'{self.xls} 列属性不一致, 请检查!!!')
            import sys
            sys.exit(1)
        return rst_dict
        

class Dict2Excel:
    '''将字典写入excel文件'''
    def __init__(self, sheet_name='sheet1'):
        # excel workbook
        self.wb = xlwt.Workbook(encoding = 'utf-8')
        # excel sheet
        self.ws = self.wb.add_sheet(sheet_name)
        
    def fill_by_dict(self, _dict):
        '''传入字典，自动按照行写入'''
        if hasattr(self, 'row_line'):
            for i, v in enumerate(_dict.values()):
                self.ws.write(self.row_line, i, str(v))
            self.row_line += 1
        else:
            self.row_line = 1
            # 填充表头
            for i, k in enumerate(_dict.keys()):
                self.ws.write(0, i, str(k))
            return self.fill_by_dict(_dict)
            
    def save(self, xls_name):
        '''将写好的文件保存'''
        self.wb.save(xls_name)


def is_corp(name):
    for t in ('厂', '馆', '社', '局', '大学', '学院', '公司', '研究院'):
        if t in name:
            return True
    return False

def get_corp_addr_map_and_names(xls_path, record=False):
    '''获取公司名和地址的字典, 和公司名'''
    xls = Excel2Dict(xls_path)
    corp_addr_map = {}
    corporation_names = []
    # 排除名单写入文件
    if record:
        fn = open(xls_path+'-exclude.txt', 'w')
    for k in range(1, xls.row_num):
        d = xls.get_dict_by_row(k)
        cnames = d['cname'].split('; ')
        types = d['type'].split('  ')
        # 去掉尾部空项
        if len(types) > 1:
            types = types[:-1]
        addr = d['addr']
        recorded = False
        for i, e in enumerate(cnames):
            # TODO: 类型长度与公司名长度不匹配导致IndexError
            # 这里只用名字长度作为个人的区分, 避免使用下标, 可能还需要改进
            if len(e) < 6 and not is_corp(e):
                # 记录排除名单到文件
                if record:
                    print(e, file=fn)
                continue
            # 去掉开头的邮编
            corp_addr = re.sub('([0-9]{6}\\s?)?', '', addr)
            if not recorded:
                corp_addr_map[e] = corp_addr
                recorded = True
            corporation_names.append(e)
    if record:
        fn.close()
    return corp_addr_map, corporation_names
    

def write_app_addrs(xls, output_xls=''):
    '''
    传入xls文件路径, 在同目录下生成_前缀的xls文件
    如上海.xls -> _上海.xls
    '''
    import os
    import sys
    sys.path.append(os.path.abspath('..'))
    from dao.CompanyAddr import CompanyAddr
    from api.cpca_api import addr_split_with_area

    corp = CompanyAddr()

    if output_xls:
        fn = output_xls
    else:
        # 新文件名
        fn = list(os.path.split(xls))
        fn[-1] = '_' + fn[-1]
        fn = os.path.join(*fn)
    # 打开工作簿获取第一张表
    if os.path.exists(fn):
        print(f'{fn}存在, 尝试从上次的进度继续...')
        wb = xlrd.open_workbook(fn)
    else:
        wb = xlrd.open_workbook(xls)

    origin_sht = wb.sheet_by_index(0)
    wb = copy(wb)
    sheet = wb.get_sheet(0)
    # 检查列数
    col_len = len(origin_sht.row(0))
    row_len = origin_sht.nrows
    if origin_sht.row(0)[-1].value != '申请人的地址':
        # 写入标头
        sheet.write(0, col_len, '申请人的地址')
    else:
        col_len -= 1
    
    print(f'正在写入到 {fn}!')
    try:
        for i in range(1, row_len):
            try:
                r = origin_sht.row(i)
                v = r[col_len].value
                # 如果未写过, 则为空或抛出IndexError
                if not v:
                    raise IndexError
                # 跳过已写的部分
                continue
            except IndexError:
                # 抛出IndexError则需要写入数据
                corp_names = origin_sht.row(i)[8].value.split('; ')
                addr = [corp.getAddr(name) for name in corp_names]
                # 语义分割地址
                addr_split = addr_split_with_area(addr)
                prov, city, area = zip(*addr_split)
                addr = ','.join(addr)
                prov = ','.join(prov)
                city = ','.join(city)
                area = ','.join(area)
                print(f'{i}/{row_len}', end='\r')
                # 写入地址
                sheet.write(i, col_len, addr)
                # 写入分散的地址(省市区)
                sheet.write(i, col_len+1, prov)
                sheet.write(i, col_len+2, city)
                sheet.write(i, col_len+3, area)
                # 写300条保存一下
                if i % 300 == 0:
                    wb.save(fn)
    except KeyboardInterrupt:
        print('被终止!')
    finally:
        wb.save(fn)
        print(f'写入完成: [{fn}]')


if __name__ == '__main__':
    # import os
    # from pprint import pprint
    # corp_addr_map, corporation_names = get_corp_addr_map_and_names(os.path.join('..', 'test', 'sh.xls'))
    # # for k, v in corp_addr_map.items():
    # pprint(corp_addr_map)
    # pprint(corporation_names)
    write_app_addrs('../2009-2015联合申请专利/2009年长三角城市群联合申请专利/安徽.xls')
    
