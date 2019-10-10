from excel.readExistInfo import get_corp_addr_map_and_names
import os
# from pprint import pprint


def _test_single_file(fn, included_pairs: [(str, str)], excluded, e2, limit=10):
    """测试模板方法
    
    fn              : 输入文件的路径
    included_pairs  : 键-值元组列表
    excluded        : 不应该出现在字典和列表的元素
    e2              : 应该出现在列表但不应该出现在字典里的
    limit           : 要求地址的前*limit*个字符一致, 默认为10
    """
    corp_addr_map, corporation_names = get_corp_addr_map_and_names(fn, True)
    assert len(corp_addr_map) < len(corporation_names)
    for i, (k, v) in enumerate(included_pairs):
        assert corp_addr_map[k][:limit] == v[:limit], f'line {i+1} error'
    for k in excluded:
        assert not k in corp_addr_map
        assert not k in corporation_names
    for k in e2:
        assert not k in corp_addr_map
    # from pprint import pprint
    # pprint(corporation_names)


def test_2009_shanghai():
    _test_single_file(os.path.join('..', '2009-2015联合申请专利', '2009年长三角城市群联合申请专利', '上海.xls'),
                    (('上海景格汽车科技有限公司', '上海市浦东新区历城路70号甲2楼A室'),
                    ('上海广为电器工具有限公司', '上海市闵行区龙吴路6200号')),
                    ('傅耀祖', '毛叔平'), 
                    ('上海广为美线电源电器有限公司',
                    '上海广为拓浦电源有限公司'))


def test_2010_anhui():
    _test_single_file(os.path.join('..', '2009-2015联合申请专利', '2010年长三角城市群联合申请专利', '安徽.xls'),
                    (('合肥丰德科技有限公司', '安徽省合肥市双凤经济开发区凤锦路'),
                    ('鑫鸿交通工业(安徽)有限公司', '安徽省宣城市飞彩科技工业园(宣城经济技术开发区内)'),
                    ('安徽海螺川崎工程有限公司', '安徽省芜湖市九华南路1007号')),
                    ('金江', '吴安新', '方卫'),
                    ('上海鑫毅交通工业有限公司',
                    '安徽铜陵海螺水泥有限公司'))


def test_2013_jiangsu():
    _test_single_file(os.path.join('..', '2009-2015联合申请专利', '2013年长三角城市群联合申请专利', '江苏1.xls'),
                    (('苏州明锐医药科技有限公司', '江苏省苏州市工业园区联丰商业广场1幢1305室'),
                    ('苏州清研微视电子科技有限公司', '江苏省苏州市吴江区交通南路1268号'),
                    ('苏州明锐医药科技有限公司', '江苏省苏州市工业园区联丰商业广场1幢1305室')),
                    ('刘力学', '耿文华', '许学农'),
                    ('苏州三元交通建设工程有限公司',
                    '中钞长城金融设备控股有限公司'))
