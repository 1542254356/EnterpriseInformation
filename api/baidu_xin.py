import requests
import json
import re
import time

from api.Api import Api


class Baidu_xin(Api):
    def __init__(self):
        pass
        # 重试次数
        # self.retryTimes = 10

    def getLocation(self, companyName):
        time.sleep(1)
        return self._getLocation(companyName, 1)

    def _getLocation(self, companyName, reTime=None):
        if reTime is None:
            reTime = 1
        url = 'https://xin.baidu.com/s/a'
        params = {
            'q': companyName
        }

        heads = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'Host': 'xin.baidu.com',
            'Referer': 'https://xin.baidu.com/s?q=%E5%A6%82%E6%9E%9C&t=0',
        }
        try:
            ret = requests.get(url, params=params)
        except requests.exceptions.ConnectionError as e:
            print(e)
            # 请求频繁导致失败
            time.sleep(reTime // 5)
            print("retry", reTime)

            return self._getLocation(companyName, reTime + 1)

        if ret.status_code != 200:
            print("请求错误：", ret.text)
            return None
        try:
            jsonret = json.loads(ret.text)
            resultList = jsonret['data']['resultList']

            if len(resultList) == 0:
                return None

            # 排除查询失败的情况
            entName = resultList[0]['entName']
            # print(entName)
            pre = re.compile(r'<.*?>', re.S)
            entName = pre.sub('', entName)

            if not self.same_company(entName, companyName):
                print("baiduxin查询失败：", companyName, "结果：", entName);
                return None

            domicile = resultList[0]['domicile']
            domicile = pre.sub('', domicile)
            return domicile
        except json.decoder.JSONDecodeError as e:
            print(e)
            # 请求频繁导致失败
            time.sleep(reTime // 5)
            print("retry", reTime)

            if reTime > 100:
                return None

            return self._getLocation(companyName, reTime + 1)


if __name__ == '__main__':
    companyNames = [
        '临海市建筑工程质量监督站',
        '乐清市乐清港湾区投资发展有限公司',
        '浙江莱美纺织印染科技有限公司',
        '中核核电运行管理有限公司',
        '上海遨提新材料技术咨询有限公司',
        '南京顿尔科技有限公司',
        '上海竹园工程管理有限公司',
        '四川理工学院',
        '北京诺斯倍尔科技发展有限责任公司'
    ]

    baidu_xin = Baidu_xin()

    for name in companyNames:
        ret = baidu_xin.getLocation(name)
        print(name, ":", ret)
