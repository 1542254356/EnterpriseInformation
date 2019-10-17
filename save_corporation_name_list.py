import os
from excel.readExistInfo import get_corp_addr_map_and_names
from utill import saveList

if __name__ == '__main__':
    corporation_names = []

    for root, dirs, files in os.walk(os.path.join('.','2009-2015联合申请专利')):
        for file in files:
            if file[-3:] == 'xls':
                _, name_list = get_corp_addr_map_and_names(os.path.join(root,file))
                corporation_names += name_list

    corporation_names = list(set(corporation_names))

    saveList('corporation_names.txt',corporation_names)

