import requests
from pprint import pprint
from bs4 import BeautifulSoup


def get_proxies():
    """从网页抓取免费代理供测试用"""
    pool = []
    # 取前十页
    for i in range(1, 11):
        proxy_url = f'https://www.kuaidaili.com/free/inha/{i}/'
        page = requests.get(proxy_url, headers={}, timeout=1)
        soup = BeautifulSoup(page.text, 'lxml')
        tlist = soup.html.body.div.find(id='content').table.tbody.find_all('tr')
        raw = [_.text[1:-1].split('\n') for _ in tlist]

        for p in raw:
            proxy = 'http://'+p[0]+':'+p[1]
            try:
                req = requests.get('http://httpbin.org/get', timeout=1, proxies={'http': proxy})
                jsn = req.json()
                origin = jsn['origin'].split(', ')[0]
                assert origin == p[0]
            except Exception as e:
                # print(e)
                # print(proxy, 'not ok')
                continue
            pool.append(proxy)
            print(proxy, 'ok')
            
    return pool


if __name__ == '__main__':
    # 抓取到的代理，可能已经过期
    proxies = [
        'http://125.123.127.213:9999',
        'http://94.191.40.157:8118',
        'http://47.94.89.87:3128',
        'http://112.74.164.135:8118',
        'http://218.104.61.246:9000',
        'http://121.232.194.60:9000',
        'http://47.99.65.77:8118',
        'http://39.106.130.141:80',
        'http://218.58.194.162:8060',
        'http://60.217.73.238:8060',
        'http://139.199.19.174:8118',
        'http://47.104.172.108:8118'
    ]
    for proxy in proxies:
        try:
            r = requests.get('http://httpbin.org/get', proxies={'http': proxy}, timeout=3)
            assert r.json()['origin'].split(', ')[0] == proxy.split(':')[1][2:]
            print('代理', proxy, 'ok!')
            # pprint(r.json())
        except AssertionError:
            print('代理地址不匹配')
        except Exception:
            continue
