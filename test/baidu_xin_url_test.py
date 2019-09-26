import requests
import json
import re




def getLocation(companyName):
    url = 'https://xin.baidu.com/s/a'
    params = {
        'q': companyName
    }
    ret = requests.get(url, params=params)
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
         '上海固柯胶带科技有限公司',
         '苏州欧普照明有限公司'
    ]

    for name in companyNames:
        ret=  getLocation(name)
        print(name,":",ret)