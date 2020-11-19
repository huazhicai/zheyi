from config.base_config import outpatient_system_code
from utils.util import capital_to_lower, quchong, filter_data

ZD_SQL = '''select ZJ_BL_ZD.ZDMC as zhenduanmingcheng, JZRQ as zhenduanriqi
                    from zj_bl_brbl left join zj_bl_zd on zj_bl_brbl.jzxh=zj_bl_zd.jzxh
                    where JZKH in {}'''

YYJL_SQL = '''select mz_cfk1.cfrq as kaiyaoshijian, ypmc as yaowumingcheng, ypgg as guige, 
                  mz_cfk2.YCJL as yicijiliang, mz_cfk2.JLDW as danwei, GYFSMC as yongfa, 
                  mz_cfk2.PL as yongyaopinlv, mz_cfk2.TZSJ as tingzhishijian from mz_cfk1
                  left join mz_cfk2 on mz_cfk1.cfsb=mz_cfk2.cfsb
                  left join GY_YPCDJG on mz_cfk2.JGXH = GY_YPCDJG.xh 
                  left join zj_gyfs on zj_gyfs.GYFSBH=mz_cfk2.FYFS
                  where mz_cfk1.jzkh in {}'''


class MenZhenData(object):

    def __init__(self, basic_info):
        "基础信息sfzh, blh, jzkh, xm, csrq"
        self.basic_info = basic_info

    def fetch(self, sql):
        import subprocess, os
        curdir = os.path.split(os.path.realpath(__file__))[0]
        url = 'jbdc:oracle:thin:@192.168.1.114:1521:ORACLE82'
        usr = 'zjhis'
        pwd = 'dec456'
        cmd = '"{}/jre1.2/bin/java.exe" -classpath "{}/oracle";"{}/oracle/classes12.zip" OracleCon {} {} {} "{}"' \
            .format(curdir, curdir, curdir, url, usr, pwd, sql)

        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        stdout, stderr = p.communicate()
        output = eval(str(stdout, encoding="GB18030"))
        output = [capital_to_lower(i) for i in output]
        return output

    def get_basic_info(self):
        sfzh, blh, jzkh, xm, csrq = self.basic_info
        out_data = []
        sql = '''select sfzh , bah as blh, jzkh, xm, csrq, ldrq from gy_brjbxxk where '''
        if sfzh:
            sfzh_sql = sql + "sfzh='{}'".format(sfzh)
            out_data.extend(self.fetch(sfzh_sql))
        if blh:
            blh_sql = sql + "bah='{}'".format(blh)
            out_data.extend(self.fetch(blh_sql))
        if jzkh:
            jzkh_sql = sql + "jzkh='{}'".format(jzkh)
            out_data.extend(self.fetch(jzkh_sql))
        if xm:
            xm_rq_sql = sql + "xm='{}'".format(xm)
            tem_data = [row_data for row_data in self.fetch(xm_rq_sql) if filter_data(self.basic_info, row_data)]
            out_data.extend(tem_data)

        seen = set()
        new_data = []
        for i in out_data:
            if i['jzkh'] not in seen:
                seen.add(i['jzkh'])
                new_data.append(i)
        return new_data

    def replace_key(self, array):
        new_array = []
        for item in array:
            new_array.append({
                60109: item['zhenduanriqi'],
                60110: item['zhenduanmingcheng'],
                60111: 2,
            })
        return new_array

    def replace_base_info_key(self, array):
        new_data = {}
        date = '1900'
        for item in array:
            if item['ldrq'] and item['ldrq'] > date:
                date = item['ldrq']  # 最新日期的基本信息
                new_data.update({
                    60104: item['xm'],
                    60105: item['sfzh'],
                    60103: item['blh'],
                    60102: item['jzkh']
                })
        return new_data

    def split_yongyaojilu(self, arry):
        koufu = []
        zhenji = []
        for item in arry:
            if item.get('yongfa') and '口' in item['yongfa']:
                koufu.append({
                    60206: item['kaiyaoshijian'],
                    60201: item['yaowumingcheng'],
                    60202: item['yicijiliang'],
                    60203: item['danwei'],
                    60205: item['yongyaopinlv'],
                    60204: item['yongfa'],
                    60208: item['tingzhishijian'],
                    60209: outpatient_system_code,  # 数据来源
                })
            elif item:
                zhenji.append({
                    60306: item['kaiyaoshijian'],
                    60301: item['yaowumingcheng'],
                    60302: item['yicijiliang'],
                    60303: item['danwei'],
                    60305: item['yongyaopinlv'],
                    60304: item['yongfa'],
                    60308: item['tingzhishijian'],
                    60309: outpatient_system_code,  # 数据来源
                })
        return koufu, zhenji

    def get_detail_data(self):
        input_array = self.get_basic_info()

        jzkh_s = [item['jzkh'] for item in input_array]
        if len(jzkh_s) == 0:
            return []  # 诊断， 口服， 针剂
        if len(jzkh_s) == 1:
            jzkh_s.append('')

        zdjl = self.fetch(ZD_SQL.format(tuple(jzkh_s)))
        zdjl = self.replace_key(zdjl)
        yyjl = self.fetch(YYJL_SQL.format(tuple(jzkh_s)))

        temp = quchong(yyjl)
        koufu, zhenji = self.split_yongyaojilu(temp)

        basic_info = self.replace_base_info_key(input_array)
        _ = [i.update(basic_info) for i in zdjl]

        return [zdjl, koufu, zhenji]


if __name__ == '__main__':
    args = ('330726193711052539', '02194917', None, '傅志法', '1937-11-05')
    menzhen = MenZhenData(args)
    menzhen.get_detail_data()
