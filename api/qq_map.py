import requests
import json


def getLocation(companyName, province="新疆"):
    url = 'https://apis.map.qq.com/ws/place/v1/search'
    params = {
        'keyword': companyName,
        'key': 'S4QBZ-YCHKP-UQ4DM-LHLYI-33TJF-32B22',
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
    if jsonret['status'] == 110:
        print("鉴权失败：", jsonret['message'])
        return None
    resultList = jsonret['data']

    # 排除查询失败的情况
    entName = resultList[0]['title']
    address = resultList[0]['address']
    # print(entName)
    # pre = re.compile('>(.*?)<')
    # entName = ''.join(pre.findall(entName))

    if entName != companyName:
        print("公司名字不符合：", companyName, "结果：", entName, "地址：", address);
        return None

    return address


if __name__ == '__main__':
    companyNames = [
        '安徽嘉联生物科技有限公司',
        '浙江华海药业股份有限公司',
        '北新集团建材股份有限公司',
        '上海江河幕墙系统工程有限公司',
        '江河创建集团股份有限公司',
        '上海固柯胶带科技有限公司',
        '苏州欧普照明有限公司'
    ]

    for name in companyNames:
        print(name, ':', getLocation(name, "北京"))
