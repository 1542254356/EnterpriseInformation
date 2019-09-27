import xlrd
import xlwt
import random
from pprint import pprint


class Excel2Dict:
    def __init__(self, xls='sh.xls', sheet_index=0):
        '''将excel转换成dict的类
        
        xls: 打开的excel文件名
        sheet_index: 第几张表'''
        book = xlrd.open_workbook(xls)
        self.sheet = book.sheet_by_index(0)
        self.title = [_.value for _ in self.sheet.row(0)]
        self.row_num = self.sheet.row_len(0)
        
    def get_dict_by_row(self, row):
        '''传入行号，返回字典'''
        r = self.sheet.row(row)
        return {
            e: r[i].value
            for i, e in enumerate(self.title)
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


if __name__ == '__main__':
    xls = Excel2Dict('sh.xls')
    xls_out = Dict2Excel('test1')
    for i in range(5):
        d = xls.get_dict_by_row(random.randint(0, xls.row_num))
        pprint(d)
        xls_out.fill_by_dict(d)
        
    xls_out.save('test.xls')
    