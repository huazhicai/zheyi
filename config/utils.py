# -*- coding:utf-8-*-
from data_structure.singleton_structure_content import new_content
from threading import Thread
from config.logger import getLogger

logger = getLogger('utils')


def quchong(array):
    seen = set()
    new_array = []
    for a in array:
        temp = tuple(a.items())
        if temp not in seen:
            seen.add(temp)
            new_array.append(a)
    return new_array


def capital_to_lower(doc):
    assert isinstance(doc, dict)
    new = {}
    for key, value in doc.items():
        new[key.lower()] = value
    return new


def filter_data(ybzl, source_data):
    # assert len(source_data) == 5

    if isinstance(ybzl, dict) and ybzl.get(20104):
        xm = ybzl.get(20104)
        sfzh = ybzl[20114]
        blh = ybzl[20103]
        jzkh = ybzl[20102]
        csrq = ybzl[20116]
    elif isinstance(ybzl, dict) and ybzl.get(10104):
        xm = ybzl.get(10104)
        sfzh = ybzl[10114]
        blh = ybzl[10103]
        jzkh = ybzl[10102]
        csrq = ybzl[10106]
    else:
        sfzh, blh, jzkh, xm, csrq = ybzl

    if isinstance(source_data, dict):
        obj_sfzh = source_data.get('sfzh')
        obj_blh = source_data.get('blh')
        obj_jzkh = source_data.get('jzkh')
        obj_xm = source_data.get('xm')
        obj_csrq = source_data.get('csrq')
    else:
        obj_sfzh, obj_blh, obj_jzkh, obj_xm, obj_csrq = source_data

    if sfzh and obj_sfzh:
        if sfzh == obj_sfzh:
            return True
        else:
            return False
    if blh and obj_blh:
        if blh == obj_blh:
            return True
        else:
            return False
    # 发现就诊卡号存在不同的情况，所以姓名日期提前验证, eg:xm=傅志法
    if obj_xm and obj_csrq:
        if xm == obj_xm and csrq and csrq[:10] == obj_csrq[:10]:
            return True

    if jzkh and obj_jzkh:
        if jzkh == obj_jzkh:
            return True
        else:
            return False


def replace_int_key(doc):
    if isinstance(doc, dict):
        new_doc = {}
        for key, val in doc.items():
            if isinstance(val, (dict, list)):
                val = replace_int_key(val)
            new_doc[str(key)] = val
        return new_doc
    if isinstance(doc, list):
        new_array = []
        for i in doc:
            new_array.append(replace_int_key(i))
        return new_array


class MyThread(Thread):
    def __init__(self, func, args):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception as e:
            logger.debug(e)
