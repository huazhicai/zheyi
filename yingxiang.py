import random

from lxml import etree

import requests
from datetime import datetime
from config.base_config import user_agent
from config.utils import filter_data

headers = {'User-Agent': random.choice(user_agent)}


class YingXiang(object):
    def __init__(self):

        self._host = 'http://192.168.33.115'

    def get_index(self, key, **post_data):
        url = self._host + '/Home/GetWorkListView'
        if post_data.get('PatientsID'):  # 提取访问详情页需要的参数
            resp = requests.post(url, data=post_data)
            paras = etree.HTML(resp.text).xpath('//table/tbody/tr/td[1]/text()')
            return paras
        elif post_data.get('PatientsAlias'):
            resp = requests.post(url, data=post_data)
            line_data = etree.HTML(resp.text).xpath('//table/tbody/tr')
            blh_s = []
            for line in line_data:
                if ''.join(line.xpath('./td[2]/text()')) == key:  # 用姓名过滤
                    blh_s.extend(line.xpath('./td[5]/text()'))
            # blh_arry = etree.HTML(resp.text).xpath('//table/tbody/tr/td[5]/text()')
            return blh_s

    def get_other_index_data(self, resp, page, key, **post_data):
        p = lambda x, y: ''.join(etree.HTML(x).xpath(y)).strip()
        total = p(resp.text, '//*[@id="hidResultTotal"]/@value')
        item_num = p(resp.text, '//*[@id="hidPageNum"]/@value')
        try:
            pages = int(total) // int(item_num) + 1
        except:
            pages = 1

        ret = []
        while page < pages and page < 10:
            page += 1
            post_data.update({"CurrentPageIndex": page})
            ret.extend(self.get_index(key, **post_data))
        return ret

    def get_data(self, key, page=1):
        url = self._host + '/Home/GetWorkListView'
        post_data = {
            'AdmissionSource': '50,10,100,1',
            'OrderBy': 'True',
            'OrderFiled': 'PatientsAlias',
            'StartTime': '2000-01-01',
            'EndTime': datetime.now().strftime('%Y-%m-%d'),
            'CurrentPageIndex': page,
        }
        if key.isdigit():  # key为病历号, 病历号检索
            post_data.update({'PatientsID': key})
            resp = requests.post(url, data=post_data)
            # 提取请求每条记录所需的参数
            paras = etree.HTML(resp.text).xpath('//table/tbody/tr/td[1]/text()')
            others = self.get_other_index_data(resp, page, key, **post_data)
            paras.extend(others)
            return paras
        else:  # key 为姓名, 用姓名搜索病历号
            name = key.encode('unicode-escape').decode().replace('\\', '%')
            post_data.update({'PatientsAlias': name})  # 姓名模糊搜索需要过滤一下
            resp = requests.post(url, post_data)
            line_data = etree.HTML(resp.text).xpath('//table/tbody/tr')
            blh_s = []
            for line in line_data:
                if ''.join(line.xpath('./td[2]/text()')) == key:  # 用姓名过滤
                    blh_s.extend(line.xpath('./td[5]/text()'))
            others = self.get_other_index_data(resp, page, key, **post_data)
            blh_s.extend(others)
            # print(blh_s)
            return blh_s

    def get_detail(self, para):
        url = self._host + '/Report/Report'
        values = para.split('|')
        keys = ('StudiesIndex', 'ResultsIndex', 'AccessionNumber', 'AdmissionID', 'PatientsID')
        param = dict(zip(keys, values))
        param.update({'DBclick': 'true'})
        resp = requests.get(url, data=param)
        p = lambda x: ''.join(etree.HTML(resp.text).xpath(x)).strip().replace('&nbsp', '')
        # [50106, 50101, 0, 50103, 50105]
        result = {
            50101: param.get('PatientsID'),  # blh
            50103: p('//*[@id="fldPatientInfo"]/table/tr[2]/td/label/text()'),  # name
            50105: p('//*[@id="fldPatientInfo"]/table/tr[7]/td/label/text()'),  # csrq
            50106: p('//*[@id="fldPatientInfo"]/table/tr[8]/td/label/text()'),  # sfz

            50205: p('//*[@id="tdContentMiddle"]/div/table/tr[3]/td/fieldset/text()'),
            50203: p('//*[@id="fldPatientInfo"]/table/tr[14]/td/label/text()'),
            50202: p('//*[@id="fldPatientInfo"]/table/tr[10]/td/label/text()'),
            50204: p('//*[@id="tdContentMiddle"]/div/table/tr[2]/td/fieldset/text()'),
            50201: p('//*[@id="fldPatientInfo"]/table/tr[18]/td/label/text()'),
        }
        main_info = {'xm': result[50103], 'blh': result[50101], 'sfzh': result[50106], 'csrq': result[50105]}
        return result, main_info

    def start(self, base_info):
        name = base_info[3]
        blh = base_info[1]

        blh_array = self.get_data(name)
        if blh: blh_array.append(blh)
        result = []
        for i in set(blh_array):
            for para in set(self.get_data(i)):
                detail_data, main_info = self.get_detail(para)
                if filter_data(base_info, main_info):  # 过滤数据
                    result.append(detail_data)
        return result


if __name__ == '__main__':
    pass
