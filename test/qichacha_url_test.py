import requests
import json
import re
from bs4 import BeautifulSoup




def getLocation(companyName):
    url = 'https://www.qichacha.com/search'
    params = {
        'key': companyName
    }

    headers = {
        "Cookie":"UM_distinctid=16d6b59df083c6-0180f297d29cd3-5373e62-1fa400-16d6b59df094c5; zg_did=%7B%22did%22%3A%20%2216d6b59e009503-05a292d90c2d02-5373e62-1fa400-16d6b59e00a2b4%22%7D; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1569464116; acw_tc=7169ab2015694641165404333eb6937813fb9bbc4f5f106b8aeb131d06; _uab_collina=156946411639350288211865; QCCSESSID=rhdt7udj6nnkoc0jrnq1klgl92; CNZZDATA1254842228=123101253-1569459642-https%253A%252F%252Fwww.baidu.com%252F%7C1571044915; hasShow=1; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201571046470247%2C%22updated%22%3A%201571046482710%2C%22info%22%3A%201571046470251%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%7D",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }
    ret = requests.get(url, params=params, headers = headers)
    if ret.status_code != 200:
        print("请求错误：",ret.text)
        return None
    jsonret = json.loads(ret.text)
    resultList = jsonret['data']['resultList']

    # 排除查询失败的情况
    entName = resultList[0]['entName']
    # print(entName)
    pre = re.compile('>(.*?)<')
    entName = ''.join(pre.findall(entName))

    if entName != name:
        print("查询失败：",name,"结果：",entName);
        return None

    return resultList[0]['domicile']



if __name__ == '__main__':
    companyNames = [
         '安徽嘉联生物科技有限公司',
         '浙江华海药业股份有限公司',
         '北新集团建材股份有限公司',
         '上海江河幕墙系统工程有限公司',
         '江河创建集团股份有限公司',
         '上海固柯胶带科技有限公司'
    ]

    for name in companyNames:
        ret=  getLocation(name)
        print(name,":",ret)