import requests
import json
from random import choice


class Proxies:
    def __init__(self, type='http'):
        self.proxies = []
        self.type = type
        self.update()

    def update(self):
        url = 'http://lab.crossincode.com/proxy/get/'
        params = {
            'num': 5000,
            'head': self.type
        }
        ret = requests.get(url, params=params)

        if ret.status_code != 200:
            print("请求错误：", ret.text)
            return

        jsonret = json.loads(ret.text)

        if 'error' in jsonret:
            print('获取ip池失败')

        proxies = jsonret['proxies']
        for proxy in proxies:
            self.proxies.append(proxy[self.type])

    def get_proxies(self):
        return self.proxies

    def get_random(self):
        return choice(self.proxies)


if __name__ == '__main__':
    http =  Proxies()

    print(http.get_random())

    url = 'http://hjwblog.com'
    proxies = {'http' : '114.99.17.184:808'}
    response = requests.get(url, proxies=proxies)
    print(requests)
