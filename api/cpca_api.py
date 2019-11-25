import cpca


def corps_to_addr(corps: [str]) -> [(str, str)]:
    '''传入公司名列表, 返回元组列表, 元组包含省市信息
    
    >>> location_str = ['杭州佩灵轴承有限公司', '乐清市乐清港湾区投资发展有限公司']
    >>> corps_to_addr(location_str)
    [('浙江省', '杭州市'), ('浙江省', '温州市')]
    '''
    df = cpca.transform(corps, umap={})
    prov = df['省'].tolist()
    city = df['市'].tolist()
    return [(e, city[i]) for i, e in enumerate(prov)]


def addr_split_with_area(corps: [str]) -> [(str, str, str)]:
    '''传入公司名列表, 返回元组列表, 元组包含省市区信息
    '''

    df = cpca.transform(corps, umap={'浦东新区':'上海市'}, cut=False, lookahead=4)
    prov = df['省'].tolist()
    city = df['市'].tolist()
    area = df['区'].tolist()
    return [(e, city[i], area[i]) for i, e in enumerate(prov)]


if __name__ == '__main__':
    s = ['上海市浦东新区','北京市朝阳区安外胜古庄2号']
    df = cpca.transform(s, umap={}, cut=False)
    print(df)
    # ret = addr_split_with_area(s)
