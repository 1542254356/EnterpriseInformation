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
    