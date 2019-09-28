import xlrd
import xlwt
import random
from pprint import pprint
import os
import sys
sys.path.append(os.path.abspath('..'))
from excel.readExistInfo import Excel2Dict, Dict2Excel


if __name__ == '__main__':
    xls = Excel2Dict('sh.xls')
    xls_out = Dict2Excel('test1')
    for i in range(5):
        d = xls.get_dict_by_row(random.randint(0, xls.row_num))
        pprint(d)
        xls_out.fill_by_dict(d)
        
    xls_out.save('test.xls')
    
