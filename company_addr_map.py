import os

import time

from excel.readExistInfo import get_corp_addr_map_and_names
from api import baidu_xin, qq_map, shunqi
from dao import companyAddr


def get_file_map():
    dic = {}
    for root, dirs, files in os.walk(os.path.join('.', '2009-2015联合申请专利')):
        for file in files:
            if file[-3:] == 'xls':
                province = file[:2]
                if province not in dic:
                    dic[province] = []
                dic[province].append(os.path.join(root, file))
                # corp_addr_map, corporation_names = get_corp_addr_map_and_names(os.path.join(root,file))
                # dic.update(corp_addr_map)
    return dic




def get_addr_by_net(corporation):
    # 从数据库读取
    addr = companyAddr.getAddr(corporation)
    if addr is not None and len(addr) > 1:
        return addr

    # 使用腾讯地图搜索
    res = qq_map.getLocation(corporation)
    if res is not None:
        return res
    # 使用百度信用搜索
    res = baidu_xin.getLocation(corporation)
    if res is not None:  # 成功找到
        return res

    # 使用顺企网搜索
    # res = shunqi.getLocation(corporation)
    # if res is not None:  # 成功找到
    #     return res

    print("error %s 没有找到" % (corporation))



if __name__ == '__main__':
    start = 0
    count = 0
    fail = 0

    with open('progress.txt', "r", encoding="utf-8") as f:
        start = int(f.readline())
        fail = int(f.readline())

    try:
        with open('corporation_names.txt', "r", encoding="utf-8") as f:
            all_lines = f.readlines()
            for line in all_lines:
                corporation = line.strip()
                count += 1
                if start > count:
                    continue

                addr = get_addr_by_net(corporation)
                if addr == None:
                    fail += 1
                print(count, fail)
                print(corporation, addr)
                if addr is not None:
                    companyAddr.add(corporation, addr)

    finally:
        with open('progress.txt', "w", encoding="utf-8") as f:
            f.write(str(count)+'\n'+str(fail))





