# -*- coding: utf-8 -*-
import random
import re

import requests
from config.base_config import user_agent

headers = {'User-Agent': random.choice(user_agent)}


class HuayanData(object):
    def __init__(self):
        self.host = 'http://192.168.50.217:8088'

    def get_requeest(self, url):
        resp = requests.get(url, headers=headers)
        return resp.json()

    def split_href(self, raw):
        ret = re.search(r'\d{4}-\d{1,2}-\d{1,2}', raw)
        if ret:
            return ret.group()
        else:
            return raw

    def get_ktv(self, patient_id):
        """
        web网页字段对应的id
        {
            'touxiqianniaosu': 300,
            'zhiliaohoutianshu': 652,
            'tizhong': 304,
            'ktv'： 308,
            'jianchariqi'： 307，
            'touxihouniaosu': 301,
            'touxishijian': 302
            'tuoshuiliang' 303,
        }
        """
        url = self.host + '/assay/listData/{}/21'.format(patient_id)
        resp = self.get_requeest(url)
        ktv_s = []
        p = lambda x, y: x[y].replace('&nbsp;', '')
        for i in resp['data']:
            ktv_s.append({
                13004: p(i, '300'),  # 透前尿素
                13002: p(i, '652'),  # 治疗后天数
                13008: p(i, '304'),  # 体重
                13003: p(i, '308'),  # kt/v
                13001: self.split_href(i['307']),  # 检查日期
                13005: p(i, '301'),  # 透后尿素
                13006: p(i, '302'),  # 透析时间
                13007: p(i, '303'),  # 脱水量
            })
        return ktv_s

    def get_urr(self, patient_id):
        """
        肾功能菜单下
        """
        url = self.host + '/assay/listData/{}/19'.format(patient_id)
        resp = self.get_requeest(url)
        urr_s = []
        p = lambda x, y: x[y].replace('&nbsp;', '')
        for i in resp['data']:
            urr_s.append({
                13108: p(i, '295'),  # 透析前尿酸
                13104: p(i, '289'),  # 透析前肌酐
                13107: p(i, '294'),  # 透析后尿素氮
                13105: p(i, '292'),  # 透析后肌酐
                13101: self.split_href(i['323']),  # 检查日期
                13103: p(i, '465'),  # urr
                13106: p(i, '293'),  # 透析前尿素氮
                13109: p(i, '463'),  # 透析后尿酸
                13102: p(i, '651'),  # 治疗后天数
            })
        return urr_s

    def get_npcr(self, patient_id):
        url = self.host + '/assay/listData/{}/36'.format(patient_id)
        resp = self.get_requeest(url)
        npcr_s = []
        p = lambda x, y: x[y].replace('&nbsp;', '')
        for i in resp['data']:
            npcr_s.append({
                13205: p(i, '538'),  # 下一次透析前BUN
                13203: p(i, '542'),  # npcr
                13208: p(i, '541'),  # 透析间期尿量
                13210: p(i, '678'),  # 体重
                13204: p(i, '537'),  # 上一次透析后BUN
                13209: p(i, '679'),  # 透析间期尿蛋白量
                13201: self.split_href(i['536']),  # 检查日期
                13207: p(i, '540'),  # 透析间期时间
                13202: p(i, '661'),  # 治疗后天数
                13206: p(i, '539'),  # 透析间期BUN
            })
        return npcr_s

    def get_ztdbbhd(self, patient_id):
        """
        铁五项
        """
        url = self.host + '/assay/listData/{}/8'.format(patient_id)
        resp = self.get_requeest(url)
        ztdbbhd_s = []
        p = lambda x, y: x[y].replace('&nbsp;', '')
        for i in resp['data']:
            ztdbbhd_s.append({
                13303: p(i, '187'),
                13307: p(i, '188'),
                13306: p(i, '186'),
                13301: self.split_href(i['252']),
                13304: p(i, '184'),
                13305: p(i, '185'),
                13302: p(i, '644'),
            })
        return ztdbbhd_s

    def start(self, patient_id):
        result = {
            'ktv': self.get_ktv(patient_id),
            'urr': self.get_urr(patient_id),
            'npcr': self.get_npcr(patient_id),
            'ztdbbhd': self.get_ztdbbhd(patient_id),
        }
        return [result]


if __name__ == '__main__':
    instance = HuayanData()
    instance.start(20614)
