import cpca
import jieba
from fuzzywuzzy.fuzz import token_sort_ratio
import re


def _case_filter(_set):
    '''对公司名列表进行处理'''
    # 需要过滤掉的关键字
    _filter = (
        '有限', '责任', '公司', '株式会社', r'\(.+?\)'
    )
    rst = []
    for case in _set:
        c = case
        for k in _filter:
            c = re.sub(k, ' ', c)
        rst.append(c)
    return rst
    

def fuzzy_match(corp1, corp2, thres=60):
    '''对两个公司名进行模糊匹配
    
    :param thres 超过这个阈值则判定为匹配
    '''
    df = cpca.transform([corp1, corp2], open_warning=False)
    df = df['地址'].tolist()
    rst = [' '.join(jieba.cut(i)) for i in df]
    rate = token_sort_ratio(*_case_filter(rst))
    print(rate, '%', end=' ')
    if rate > thres:
        return True
    
    return False
