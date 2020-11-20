# -*- coding: utf-8 -*-
import json

from utils.util import capital_to_lower, filter_data

BASE_SQL = '''select blh, patientid as jzkh, PATIENTNAME as xm, birthday as csrq, 
                    CHECKTIME as jianyanshijian, EXAMINAIM as jianyanmudi, SAMPLENO as sample 
                    from L_PATIENTINFO  where blh='{}' or patientid='{}' or patientname='{}' '''

DETAIL_SQL = '''select sampleno as sample, B.CHINESENAME as jianyanxiangmu,B.ENGLISHAB as jianyanxiangmuen,TESTRESULT as ceshijieguo,
        REFLO as cankaodixian,REFHI as cankaogaoxian,MEASURETIME as jianyanshijian,L_TESTRESULT.UNIT as danwei 
        from L_TESTRESULT left join L_TESTDESCRIBE B on L_TESTRESULT.TESTID=B.TESTID  where SAMPLENO in {} '''


class LisData(object):
    def __init__(self, base_info, config_data):
        self.base_info = base_info

        self.config_data = config_data
        self.out_data = {}
        self.record_samples = []

    def fetch(self, sql):
        import subprocess, os
        curdir = os.path.split(os.path.realpath(__file__))[0]
        url = 'jbdc:oracle:thin:@192.168.1.7:1521:jyk'
        usr = 'zjhis'
        pwd = 'zjhis'
        cmd = '"{}/jre1.2/bin/java.exe" -classpath "{}/oracle";"{}/oracle/classes12.zip" OracleCon {} {} {} "{}"' \
            .format(curdir, curdir, curdir, url, usr, pwd, sql)
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        stdout, stderr = p.communicate()

        output = eval(str(stdout, encoding="GB18030"))
        output = [capital_to_lower(i) for i in output]
        return output

    def get_base_info(self):
        sfzh, blh, jzkh, xm, csrq = self.base_info
        sql = BASE_SQL.format(blh, jzkh, xm)
        out_data = [row_data for row_data in self.fetch(sql) if filter_data(self.base_info, row_data)]
        return out_data

    def get_test_results(self):
        sample_map_results = {}

        input_array = self.get_base_info()
        samples = [i['sample'] for i in input_array if len(i['sample']) > 5]
        if len(samples) == 0:
            return sample_map_results

        # 当样本号超过1000时，oracle 有限制
        sample_assemble = []
        while len(samples) > 1000:
            sample_assemble.append(samples[:1000])
            samples = samples[1000:]

        if len(samples) == 1:
            samples.append('')

        sample_assemble.append(samples)

        test_results = []
        for samps in sample_assemble:
            test_results.extend(self.fetch(DETAIL_SQL.format(tuple(samps))))

        for result in test_results:
            if sample_map_results.get(result['sample']):
                sample_map_results[result['sample']].append(result)
            else:
                sample_map_results[result['sample']] = [result]

        return sample_map_results

    def extract_data_with_field(self, data):
        name = data['jianyanxiangmu']
        unit = data['danwei']
        value = data["ceshijieguo"]
        date = data["jianyanshijian"]
        for item in self.config_data.values():
            if (item['unit'] and item['unit'] == unit) or not item['unit']:
                if name in item["source"]:
                    item.update({
                        "value": value,
                        "date": date
                    })
                    return item

    def insert_data(self, doc, sample):
        if doc is None:
            return
        parent_id = doc.get('parent_id')
        if not self.out_data.get(parent_id):
            self.out_data[parent_id] = []

        if sample + parent_id in self.record_samples:
            self.out_data[parent_id][-1].update({
                doc['id']: doc['value'],
                doc['date_key']: doc['date']
            })
        else:
            self.out_data[parent_id].append({
                doc['id']: doc['value'],
                doc['date_key']: doc['date'],
            })
            self.record_samples.append(sample + parent_id)

    def start(self):
        for sample, test_items in self.get_test_results().items():
            for item in test_items:
                ret_data = self.extract_data_with_field(item)
                self.insert_data(ret_data, sample)
        if self.out_data:
            return {"zhyl1500000": {"zhyl1510000": self.out_data}}


if __name__ == '__main__':
    args = ('330622194208253417', '02614770', None, '陈寿康', '1942-08-25')
    with open('config/jianyan_field.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    lis_data = LisData(args, config)
    lis_data.start()
