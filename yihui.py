# -*- coding: utf-8 -*-
import random
import re

import requests
from lxml import etree
from config.base_config import user_agent
from config.utils import quchong, filter_data

headers = {'User-Agent': random.choice(user_agent)}


class YihuiSystem(object):
    def __init__(self):

        self._host = 'http://192.168.2.155:6060'

    def search_patient(self, blh):
        """
        用病历号搜索病人记录
        血透过来病历号，就是次网页的patientId
        """
        url = self._host + '/EgretWS/EgretService'
        request_data = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><getArchivedPatientBySeries xmlns="http://egret/"><patientId xmlns="">{}</patientId><series xmlns="">0</series><patientName xmlns="" /><cliCode xmlns="">EgretPC</cliCode><updateNo xmlns="">122</updateNo></getArchivedPatientBySeries></soap:Body></soap:Envelope>'.format(
            blh)
        resp = requests.post(url, data=request_data, headers=headers)
        series_code = etree.HTML(resp.text).xpath('//return/series/text()')
        # print(series_code)
        return series_code

    def get_request(self, binglihao, series, request_data):
        url = self._host + '/EgretWS/EgretService'
        request_body = request_data.format(binglihao, series)
        try:
            response = requests.post(url, data=request_body, headers=headers)
            if response.status_code == 200 and response:
                return response.text
        except Exception as e:
            pass
            # print('get_data', e)

    def parse_tiwendang_data(self, response):
        doc = etree.HTML(response).xpath('//return')
        p = lambda x, y: ''.join(x.xpath(y)).strip()
        for i in doc:
            yield {
                'valtype': p(i, './vitalsignstype/text()'),
                'shuzhi': p(i, './vitalsignsval/text()') + p(i, './unit/text()'),
                'shijian': p(i, './excutetime/text()'),
                'hightval': p(i, './vitalsignshightval/text()'),
            }

    def parse_xuetang_data(self, response):
        doc = etree.HTML(response).xpath('//return')
        p = lambda x, y: ''.join(x.xpath(y)).strip()
        xuetang = [{71002: p(i, './val/text()') + p(i, './unit/text()'),
                    71001: p(i, './createtime/text()')} for i in doc]
        return xuetang

    def get_data(self, blh):
        tiwendang_para = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><gettemperature xmlns="http://egret/"><type xmlns="">4001</type><type xmlns="">4002</type><type xmlns="">4032</type><type xmlns="">4030</type><type xmlns="">4003</type><type xmlns="">4008</type><type xmlns="">4004</type><type xmlns="">4006</type><type xmlns="">4007</type><type xmlns="">4005</type><type xmlns="">4031</type><type xmlns="">4009</type><type xmlns="">4010</type><type xmlns="">4011</type><type xmlns="">4040</type><type xmlns="">4041</type><type xmlns="">4042</type><type xmlns="">4046</type><type xmlns="">4033</type><type xmlns="">4021</type><type xmlns="">4022</type><type xmlns="">4023</type><type xmlns="">4024</type><type xmlns="">4025</type><type xmlns="">4026</type><type xmlns="">4091</type><type xmlns="">4092</type><type xmlns="">4093</type><type xmlns="">4094</type><type xmlns="">4020</type><patient_id xmlns="">{}</patient_id><series xmlns="">{}</series><cliCode xmlns="">EgretPC</cliCode><updateNo xmlns="">122</updateNo></gettemperature></soap:Body></soap:Envelope>'
        xuetang_para = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><listSimpleReportsByPatientId xmlns="http://egret/"><patientId xmlns="">{}</patientId><series xmlns="">{}</series><startTime xmlns="">2005-12-11T00:00:00</startTime><endTime xmlns="">2060-12-31T23:59:59+08:00</endTime><cliCode xmlns="">EgretPC</cliCode><updateNo xmlns="">122</updateNo></listSimpleReportsByPatientId></soap:Body></soap:Envelope>'
        series_code = self.search_patient(blh)

        tiwen = []  # 4001
        maibo = []  # 4002
        huxi = []  # 4003
        xueya = []  # 4008
        suoya = []  # 4008
        zhangya = []  # 4008
        tizhong = []  # 4009
        shengao = []  # 4031
        niaoliang = []  # 4005
        xuetang = []
        # print(set(series_code))
        if series_code:
            for code in set(series_code):  # 一个病人多次住院记录
                tiwendang_resp = self.get_request(blh, code, tiwendang_para)
                for itm in self.parse_tiwendang_data(tiwendang_resp):
                    valtype = itm.pop('valtype')
                    hightval = itm.pop('hightval')  # 舒张压
                    temp_doc = {}
                    if valtype == '4001':
                        temp_doc[70201] = itm['shijian']
                        temp_doc[70202] = itm['shuzhi']
                        tiwen.append(temp_doc)
                    elif valtype == '4002':
                        temp_doc[70101] = itm['shijian']
                        temp_doc[70102] = itm['shuzhi']
                        maibo.append(temp_doc)
                    elif valtype == '4003':
                        temp_doc[70301] = itm['shijian']
                        temp_doc[70302] = itm['shuzhi']
                        huxi.append(temp_doc)
                    elif valtype == '4008':
                        temp_doc[70411] = itm['shijian']
                        temp_doc[70412] = itm['shuzhi']
                        suoya.append(temp_doc)

                        zhangya.append({
                            70401: itm['shijian'],
                            70402: hightval+'mmHg'
                        })
                    elif valtype == '4009':
                        temp_doc[70601] = itm['shijian']
                        temp_doc[70602] = itm['shuzhi']
                        tizhong.append(temp_doc)
                    elif valtype == '4031':
                        temp_doc[70501] = itm['shijian']
                        temp_doc[70502] = itm['shuzhi']
                        shengao.append(temp_doc)
                    elif valtype == '4005':
                        temp_doc[70701] = itm['shijian']
                        temp_doc[70702] = itm['shuzhi']
                        niaoliang.append(temp_doc)

                xuetang_resp = self.get_request(blh, code, xuetang_para)
                xuetang.extend(self.parse_xuetang_data(xuetang_resp))

            info = self.patient_info(blh)
            result = {
                # 'binglihao': blh,
                't': quchong(tiwen),
                'p': quchong(maibo),
                'r': quchong(huxi),
                'suoya': quchong(suoya),
                'zhangya': quchong(zhangya),
                'tizhong': quchong(tizhong),
                'shengao': quchong(shengao),
                'niaoliang': quchong(niaoliang),
                'xuetang': quchong(xuetang),
                'ruliang': [],
                'chuliang': [],
            }
            # result.update(info)
            return result

    def patient_info(self, blh):
        url = self._host + '/EgretWS/EgretService'
        para = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><getPatientById xmlns="http://egret/"><patientId xmlns="">{}</patientId><cliCode xmlns="">EgretPC</cliCode><updateNo xmlns="">122</updateNo></getPatientById></soap:Body></soap:Envelope>'.format(
            blh)
        resp = requests.post(url, data=para, headers=headers)
        q = lambda x: ''.join(etree.HTML(resp.text).xpath(x)).strip()
        info = {
            'xm': q('//return/patient/name/text()'),
            'sfzh': q('//return/sfzhm/text()'),
            'blh': blh,
            'jzkh': None,
            'csrq': re.sub(r'T.*', '', q('//return/patient/dob/text()')),
        }
        # return info
        return info

    def search_patient_with_name(self, name):
        url = self._host + '/EgretWS/EgretService'
        name = name.encode('utf-8').decode('latin1')
        para = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><getArchivedPatientBySeries xmlns="http://egret/"><patientId xmlns="" /><series xmlns="">0</series><patientName xmlns="">{}</patientName><cliCode xmlns="">EgretPC</cliCode><updateNo xmlns="">122</updateNo></getArchivedPatientBySeries></soap:Body></soap:Envelope>'.format(
            name)
        resp = requests.post(url, data=para, headers=headers)
        blh_array = etree.HTML(resp.text).xpath('//patientid/text()')
        return blh_array

    def start(self, base_info):
        name = base_info[3]
        blh = base_info[1]

        blh_set = set(self.search_patient_with_name(name))
        blh_array = [i for i in blh_set if filter_data(base_info, self.patient_info(i))]  # 过滤数据
        if blh: blh_array.append(blh)
        result = [self.get_data(i) for i in set(blh_array) if i]

        return result


if __name__ == '__main__':
    instance = YihuiSystem()
    instance.start('')
