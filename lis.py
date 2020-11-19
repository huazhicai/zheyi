# -*- coding: utf-8 -*-
from utils.util import capital_to_lower, filter_data

BASE_SQL = '''select blh, patientid as jzkh, PATIENTNAME as xm, birthday as csrq, 
                    CHECKTIME as jianyanshijian, EXAMINAIM as jianyanmudi, SAMPLENO as yangbenhao 
                    from L_PATIENTINFO  where blh='{}' or patientid='{}' or patientname='{}' '''

DETAIL_SQL = '''select sampleno as yangbenhao, B.CHINESENAME as jianyanxiangmu,B.ENGLISHAB as jianyanxiangmuen,TESTRESULT as ceshijieguo,
        REFLO as cankaodixian,REFHI as cankaogaoxian,MEASURETIME as jianyanshijian,L_TESTRESULT.UNIT as danwei 
        from L_TESTRESULT left join L_TESTDESCRIBE B on L_TESTRESULT.TESTID=B.TESTID  where SAMPLENO in {} '''


class LisData(object):
    def __init__(self, base_info):
        self.base_info = base_info

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

    def replace_jieguo_key(self, array):
        new_array = []
        for item in array:
            new_array.append({
                40301: item['jianyanxiangmu'],
                40302: item['ceshijieguo'],
                40303: item['cankaodixian'],
                40304: item['cankaogaoxian'],
                40305: item['jianyanshijian'],
                40203: item['danwei']
            })
        return new_array

    def replace_key(self, array):
        new_array = []
        for item in array:
            new_array.append({
                40106: item['blh'],
                40107: item['jzkh'],
                40103: item['csrq'],
                40101: item['xm'],
                40105: item['jianyanmudi'],
                40201: item['yangbenhao'],
                'jieguo': self.replace_jieguo_key(item['jieguo'])
            })
        return new_array

    def get_detail_data(self):
        input_array = self.get_base_info()
        yangbenhao_s = [i['yangbenhao'] for i in input_array]
        if len(yangbenhao_s) == 0:
            return []

        # 当样本号超过1000时，oracle 有限制
        yangbenhao_list = []
        while len(yangbenhao_s) > 1000:
            yangbenhao_list.append(yangbenhao_s[:1000])
            yangbenhao_s = yangbenhao_s[1000:]

        if len(yangbenhao_s) == 1:
            yangbenhao_s.append('')
        yangbenhao_list.append(yangbenhao_s)
        jieguo = []
        for ybh in yangbenhao_list:
            jieguo.extend(self.fetch(DETAIL_SQL.format(tuple(ybh))))

        for item in input_array:
            item['jieguo'] = [i for i in jieguo if i['yangbenhao'] == item['yangbenhao']]

        out_data = self.replace_key(input_array)
        return out_data


if __name__ == '__main__':
    args = ('330726193711052539', '02194917', None, '傅志法', '1937-11-05')
    lis_data = LisData(args)
    lis_data.get_detail_data()
