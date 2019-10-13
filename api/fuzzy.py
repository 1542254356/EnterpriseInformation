import cpca
import jieba
from fuzzywuzzy.fuzz import token_sort_ratio
import re


def fuzzy_match(corp1, corp2, thres=.5):
    df = cpca.transform([corp1, corp2])
    df = df['地址'].tolist()
    rst = [' '.join(jieba.cut(i)) for i in df]
    rate = token_sort_ratio(*rst)
    print(rst, rate)
    if rate > thres:
        return True
    
    return False


if __name__ == '__main__':
    # 判定为相似的测试例
    test_set = (
        ('四川省纳溪供电有限责任公司', '纳溪供电公司'),
        ('上海仪器仪表自控系统检验测试所', '上海仪器仪表自控系统检验测试所有限公司'),
        ('快捷半导体公司', '快捷半导体(苏州)有限公司'),
        ('上海东浩国际服务贸易(集团)有限公司', '上海东浩兰生国际服务贸易(集团)有限公司'),
    )
    # 判定为不相似的测试例
    test_n_set = (
        ('铃木锻工株式会社', '唐山丰石汽车配件有限公司'),
    )
    # 需要过滤掉的关键字
    _filter = (
        '有限', '责任', '公司', '株式会社', '\(.+?\)'
    )
    def case_filter(_set):
        rst = []
        for case in _set:
            c = case
            for k in _filter:
                c = re.sub(k, ' ', c)
            rst.append(c)
        return rst


    for case in test_set:
        try:
            print(*case)
            case = case_filter(case)
            assert fuzzy_match(*case), '被判为不相似'
            print('判定为相似:', *case)
        except AssertionError:
            continue

    for case in test_n_set:
        try:
            print(*case)
            case = case_filter(case)
            assert not fuzzy_match(*case), '被判为相似'
            print('判定为不相似:', *case)
        except AssertionError:
            continue 