import os

from dao import companyAddr
from excel.readExistInfo import get_corp_addr_map_and_names





if __name__ == '__main__':
    corp_addr_map = {}

    for root, dirs, files in os.walk(os.path.join('.', '2009-2015联合申请专利')):
        for file in files:
            if file[-3:] == 'xls':
                print(os.path.join(root, file))
                name_map, _ = get_corp_addr_map_and_names(os.path.join(root, file))
                corp_addr_map.update(name_map)


    companyAddr.saveDic(corp_addr_map)