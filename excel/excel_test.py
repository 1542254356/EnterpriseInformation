import pytest
from excel.readExistInfo import get_corp_addr_map_and_names


import os
# from pprint import pprint

def _test_single_file(fn, included_pairs, excluded, limit=10):
    corp_addr_map, corporation_names = get_corp_addr_map_and_names(fn)
    for i, (k, v) in enumerate(included_pairs):
        assert corp_addr_map[k][:limit] == v[:limit], f'line {i+1} error'
    for k in excluded:
        assert k not in corp_addr_map
        assert k not in corporation_names
    # from pprint import pprint
    # pprint(corporation_names)


def test_2015_shanghai():
    _test_single_file(os.path.join('..', '2009-2015联合申请专利', '2009年长三角城市群联合申请专利', '上海.xls'),
                    (('上海景格汽车科技有限公司', '上海市浦东新区历城路70号甲2楼A室'),
                    ('上海广为电器工具有限公司', '上海市闵行区龙吴路6200号'),
                    ('上海广为美线电源电器有限公司', '上海市闵行区龙吴路6200号'),
                    ('上海广为拓浦电源有限公司', '上海市闵行区龙吴路6200号'),),
                    ('傅耀祖', '毛叔平'))


def test_2016_anhui():
    pairs = [(i, '安徽省芜湖市九华南路1007号') for i in '安徽海螺川崎工程有限公司; 安徽海螺川崎节能设备制造有限公司; 安徽铜陵海螺水泥有限公司'.split('; ')]
    _test_single_file(os.path.join('..', '2009-2015联合申请专利', '2010年长三角城市群联合申请专利', '安徽.xls'),
                    (('合肥丰德科技有限公司', '安徽省合肥市双凤经济开发区凤锦路'),
                    *pairs),
                    ('金江', '吴安新', '方卫'))
