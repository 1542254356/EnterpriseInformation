import os
from excel.readExistInfo import get_corp_addr_map_and_names



if __name__ == '__main__':
    for root, dirs, files in os.walk(os.path.join('.','2009-2015联合申请专利')):
        for file in files:
            corp_addr_map, corporation_names = get_corp_addr_map_and_names(os.path.join(root,file))
            pass
