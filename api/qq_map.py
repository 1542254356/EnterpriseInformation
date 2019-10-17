import requests
import json
from api.Api import Api


class QQ_map(Api):

    def getLocation(self, companyName):
        return self._getLocation(companyName)

    def _getLocation(self, companyName, province="新疆"):
        url = 'https://apis.map.qq.com/ws/place/v1/search'
        params = {
            'keyword': companyName,
            'key': 'D27BZ-SOTKU-NJ3VN-BTTWX-LE2EV-DYFO7',
            'boundary': 'region(%s,1)' % (province)
        }

        headers = {
            'Referer': 'http://hjwblog.com'
        }
        ret = requests.get(url, params=params, headers=headers)
        if ret.status_code != 200:
            print("请求错误：", ret.text)
            return None
        jsonret = json.loads(ret.text)
        if jsonret['status'] != 0:
            print("qq_map api调用失败：", jsonret['status'], jsonret['message'])
            return None

        resultList = jsonret['data']

        if len(resultList) == 0:
            return None

        # 排除查询失败的情况
        entName = resultList[0]['title']
        address = resultList[0]['address']
        # print(entName)
        # pre = re.compile('>(.*?)<')
        # entName = ''.join(pre.findall(entName))

        if not self.same_company(entName, companyName):
            print("qq_map公司名字不符合：", companyName, "结果：", entName, "地址：", address);
            return None

        return address


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

    qq_map = QQ_map()

    for name in companyNames:
        print(name, ':', qq_map.getLocation(name))
