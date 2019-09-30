# 读取excel文件里面已有的公司名字和地址映射

import xlrd
import xlwt
import random


class Excel2Dict:
    def __init__(self, xls='test/sh.xls', sheet_index=0):
        '''将excel转换成dict的类
        
        xls: 打开的excel文件名
        sheet_index: 第几张表'''
        book = xlrd.open_workbook(xls)
        self.sheet = book.sheet_by_index(0)
        self.title = [_.value for _ in self.sheet.row(0)]
        self.row_num = self.sheet.nrows
        
    def get_dict_by_row(self, row):
        '''传入行号，返回字典'''
        r = self.sheet.row(row)
        return {
            'cname': r[8].value,
            'addr': r[11].value,
            'type': r[12].value
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


def get_corp_addr_map_and_names(xls_path):
    '''获取公司名和地址的字典, 和公司名'''
    xls = Excel2Dict(xls_path)
    corp_addr_map = {}
    corporation_names = []
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
            if len(e) < 4:
                print('跳过', e)
                continue
            corp_addr = addr.split(' ')[-1]
            corp_addr_map[e] = corp_addr
            corporation_names.append(e)
    return corp_addr_map, corporation_names
    

if __name__ == '__main__':
    import os
    from pprint import pprint
    corp_addr_map, corporation_names = get_corp_addr_map_and_names(os.path.join('..', 'test', 'sh.xls'))
    pprint(corp_addr_map)
    pprint(corporation_names)
    
