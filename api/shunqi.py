import requests
import json
from bs4 import BeautifulSoup

from api.Api import Api

class Shunqi(Api):
    def getLocation(self,companyName):
        return self._getLocation(companyName)

    def _getLocation(self, companyName):
        url = 'http://so.11467.com/cse/search'
        params = {
            's': '662286683871513660',
            'ie': 'utf-8',
            'q': companyName
        }
        ret = requests.get(url, params=params)
        ret.encoding = ret.apparent_encoding

        if ret.status_code != 200:
            print("请求错误：", ret.text)
            return None

        soup = BeautifulSoup(ret.text, "html.parser")
        div = soup.find(attrs={'class': 'result f s0'})
        if div is None:
            return None
        try:
            title = div.h3.a
        except Exception as e:
            print(e)
            return None

        resultName = title.text

        if not self.same_company(resultName, companyName):
            print("shunqi查询失败：", companyName, resultName);
            return None

        a = div.h3.a
        link = a.attrs['href']

        headers = {
            "Cookie": "ASPSESSIONIDQSXBSRBT=OOACNLIALKPLBDPPMCBNKLKD; ASPSESSIONIDQSXCRRBS=ELCNBCNAEEAIGEODEHJMKOCJ; Hm_lvt_819e30d55b0d1cf6f2c4563aa3c36208=1570885529; Hm_lpvt_819e30d55b0d1cf6f2c4563aa3c36208=1570885816",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        }

        # print(link)

        ret = requests.get(link, headers=headers)
        if ret.status_code != 200:
            print("请求错误：", ret.text)
            return None

        soup = BeautifulSoup(ret.text, "html.parser")
        dl = soup.find(attrs={'class': 'codl'})
        dd = dl.dd

        addr = dd.text
        addrs = addr.split(' ')

        if len(addrs) < 2:
            return None

        return addrs[1]









if __name__ == '__main__':
    companyNames = [
        '杭州佩灵轴承有限公司',
        '乐清市乐清港湾区投资发展有限公司',
        '浙江莱美纺织印染科技有限公司',
        '中核核电运行管理有限公司',
        '上海遨提新材料技术咨询有限公司',
        '南京顿尔科技有限公司',
        '上海竹园工程管理有限公司',
        '四川理工学院',
        '北京诺斯倍尔科技发展有限责任公司'
    ]

    for name in companyNames:
        ret = getLocation(name)
        print(name, ":", ret)