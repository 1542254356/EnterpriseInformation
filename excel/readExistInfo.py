# 读取excel文件里面已有的公司名字和地址映射

import xlrd
import xlwt
import random
import re


class Excel2Dict:
    def __init__(self, xls='test/sh.xls', sheet_index=0):
        '''将excel转换成dict的类
        
        xls: 打开的excel文件名
        sheet_index: 第几张表'''
        book = xlrd.open_workbook(xls)
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
        return {
            'cname': r[self.cname_col].value,
            'addr' : r[self.addr_col].value,
            'type' : r[self.type_col].value
        }
        

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
    for t in ('厂', '馆', '社', '大学', '学院', '公司', '研究院'):
        if t in name:
            return True
    return False

def get_corp_addr_map_and_names(xls_path):
    '''获取公司名和地址的字典, 和公司名'''
    xls = Excel2Dict(xls_path)
    corp_addr_map = {}
    corporation_names = []
    # 排除名单写入文件
    with open(xls_path+'-exclude.txt', 'w') as f:
        for k in range(1, xls.row_num):
            d = xls.get_dict_by_row(k)
            cnames = d['cname'].split('; ')
            types = d['type'].split('  ')
            # 去掉尾部空项
            if len(types) > 1:
                types = types[:-1]
            addr = d['addr']
            for i, e in enumerate(cnames):
                # TODO: 类型长度与公司名长度不匹配导致IndexError
                # 这里只用名字长度作为个人的区分, 避免使用下标, 可能还需要改进
                if len(e) < 6 and not is_corp(e):
                    continue
                # 去掉开头的邮编
                corp_addr = re.sub('([0-9]{6}\\s?)?', '', addr)
                corp_addr_map[e] = corp_addr
                corporation_names.append(e)
    return corp_addr_map, corporation_names
    

if __name__ == '__main__':
    import os
    from pprint import pprint
    corp_addr_map, corporation_names = get_corp_addr_map_and_names(os.path.join('..', 'test', 'sh.xls'))
    # for k, v in corp_addr_map.items():
    pprint(corp_addr_map)
    pprint(corporation_names)
    
