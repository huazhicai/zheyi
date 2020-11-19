# 在requests headers中，禁用删除If - Modified-Since 和If-None-Natch 这两项

import requests
from utils.logger import getLogger
from utils.crack_password import crack_pwd
from utils.util import filter_data, quchong

logger = getLogger('new_his')

USER = '10357'
PASSWORD = '123456'
ACCESS_TOKEN = None
K1 = None
K2 = None


def login():
    global ACCESS_TOKEN, K1, K2
    url = 'http://his.zheyi.com/app-sso/oauth/token'
    params = {
        'grant_type': 'password',
        'username': USER,
        'password': crack_pwd(PASSWORD),
        'verifyCode': '',
        'sessionId': '',
    }
    basic_authorize = {'Authorization': 'Basic bm9idWc6Z2l2ZW1lZml2ZQ==', }
    response = requests.post(url, headers=basic_authorize, params=params)
    body = response.json()
    ACCESS_TOKEN = body['body'].get('access_token')
    if ACCESS_TOKEN is None:
        logger.info('登录失败 {}'.format(body))
        assert ACCESS_TOKEN
    # 向服务器发送token， 认证token
    authorize = {'Authorization': 'Bearer {}'.format(ACCESS_TOKEN), }
    setting_url = 'http://his.zheyi.com/app-portal/get/default/setting'
    response = requests.post(setting_url, headers=authorize)
    result = response.json()

    K1 = str(result['body']['defaultIns'])
    K2 = str(result['body']['defaultLoc'])


class NewHis(object):
    def __init__(self, source_info):
        self.source_info = source_info
        self.user = '10357'
        self.password = '123456'
        self.host = 'http://his.zheyi.com'
        login()

        assert ACCESS_TOKEN
        self.authorize = {'Authorization': 'Bearer {}'.format(ACCESS_TOKEN),
                          'k2': K2,
                          'k1': K1,
                          }

    def get_request(self):
        pass

    def search_patient(self, search_key, retry_flag=True):
        url = self.host + '/app-station-manage/manage/medicalRecord/query/patientinfo'
        json_data = {'searchText': search_key}
        response = requests.post(url, headers=self.authorize, json=json_data)
        result = response.json()
        data = result['body']['data']
        return data

    def check_patient(self, doc):
        """数据验证"""
        url = self.host + '/app-station-manage/medicalRecord/getInpatientInfo'
        json_data = {"inpatientId": doc['inhospitalPatientId'],
                     "masterPatientIndex": doc['masterPatientIndex'],
                     "type": '2', }
        response = requests.post(url, headers=self.authorize, json=json_data)
        result = response.json()
        data = result['body']
        if result['code'] == 2000 and data:
            base_info = (data['idCardNo'], data['medicalRecordNo'], '', data['patientName'], data['birthdate'])
            if filter_data(self.source_info, base_info):
                patientInfo = {
                    30101: data['patientName'],
                    30102: data['gender'],
                    30104: data['medicalRecordNo'],
                    30110: data['birthdate'],
                    30178: data['age'],
                    30111: data['countryName'],

                    30117: data['nationDesc'],
                    30119: data['idCardNo'],
                    30106: None,  # 医疗保险支付方式
                    30107: data['costTypeName'],
                    30115: data['professionDesc'],
                    30118: data['marriageStatusDesc'],
                    30120: data['presentAddress'],
                    # 30126: p_2('TxtDwdh'),  # 单位电话
                    30121: data['workName'],
                    30122: data['workAddress'],
                    30128: data['hospitalizedWayDesc'],
                    30129: data['hospitalizedDate'],
                    30133: data['hospitalizedMainDiagnose'],
                    30182: 3,  # 数据来源
                    30131: data['outHospitalDate'],
                    30130: data['hospitalDays'],

                    30136: data['injuryPoisoningReason'],
                    30138: None,
                    # 30139: p_2('TxtBlh'),  # 病理号
                    30174: data['aboType'],
                    30140: data['hbsAg'],  # 0:阴性 1：阳性 null:未做
                    30141: data['hcvAb'],
                    30142: data['hivAb'],
                    30143: data['tpha'],
                    30144: data['infectiousReport'],
                    30175: data['rhType'],
                    30137: data['allgergyDesc'],
                    30173: data['outHospitalWay'],
                    30176: data['hospitalizedAgain'],
                    30177: '入院前: {}'.format(data['beforeHospitalizedComa']) + '入院后: {}'.format(
                        data['afterHospitalizedComa']),
                    'lxr': [{
                        30124: data['linkmanName'],
                        30125: data['linkmanAddress'],
                        30126: data['linkmanPhoneNo'],
                        30180: data['linkTypeName']
                    }],
                }
                index_id = data['id']
                return patientInfo, index_id
        return '', False

    def get_diagnoses(self, doc, index_id):
        diagnoses_container = []
        diagnose_url = self.host + '/app-station-manage/medicalRecord/getDiagnose'
        json_data = {"inpatientId": doc['inhospitalPatientId'],
                     "masterPatientIndex": doc['masterPatientIndex'],
                     'medicalRecordMasterId': str(index_id),
                     "type": '2', }
        diagnose_response = requests.post(diagnose_url, headers=self.authorize, json=json_data)
        data = diagnose_response.json()
        diagnose_data = data['body']['diagnoses']
        map_key = {1: '有', 2: '未确认'}
        if diagnose_data:
            main_diagnose = diagnose_data[0].get('mainDiagnose')
            if main_diagnose:
                main_diagnose_data = {
                    30181: '主要诊断',
                    30134: main_diagnose['diagnoseName'],
                    30132: map_key.get(main_diagnose['hospitalizedConditions']),
                    30135: main_diagnose['diagnoseIcd'],
                }
                diagnoses_container.append(main_diagnose_data)

            sub_diagnoses = diagnose_data[0].get('subDiagnose')
            if sub_diagnoses:
                for sub_diagnose in sub_diagnoses:
                    diagnoses_container.append({
                        30181: '其他要诊断',
                        30134: sub_diagnose['diagnoseName'],
                        30132: map_key.get(sub_diagnose['hospitalizedConditions']),
                        30135: sub_diagnose['diagnoseIcd'],
                    })

        return diagnoses_container

    def get_operation(self, doc, index_id):
        operations_container = []
        operation_url = self.host + '/app-station-manage/medicalRecord/getOperation'
        json_data = {"inpatientId": doc['inhospitalPatientId'],
                     "masterPatientIndex": doc['masterPatientIndex'],
                     'medicalRecordMasterId': str(index_id),
                     "type": '2', }
        response = requests.post(operation_url, headers=self.authorize, json=json_data)
        source_data = response.json()
        data = source_data['body']
        operations = data.get('operationList')
        if operations:
            for operation in operations:
                operations_container.append({
                    30145: operation['icd'],
                    30146: operation['operationDate'],
                    30147: operation['operationName'],
                    30148: operation['anesthesiaType'],
                    30149: operation['healName'],
                })
        return operations_container

    def get_fee(self, doc):
        fee_url = self.host + '/app-hospitalized-register/recordSubject/detailAmountForRecordSubject'
        json_data = {"inhospitalPatientId": doc['inhospitalPatientId'], }
        response = requests.post(fee_url, headers=self.authorize, json=json_data)
        source_data = response.json()
        data = source_data['body']
        fee = {
            30150: data['totalAmount'],
            30151: data['generalMedicalServiceFee'],
            30152: data['nursingFee'],
            30153: data['westernMedicineFee'],
            30154: data['chinesePatentMedicineFee'],
            30155: data['chineseHerbalMedicineFee'],
            30156: data['imagingDiagnosisFee'],
            30157: data['laboratoryDiagnosticFee'],
            30158: data['albuminProductFee'],
            30159: data['bloodFee'],
            30161: data['surgeryFee'],
            30162: data['globulinProductFee'],
            30163: data['pathologicalDiagnosisFee'],
            30164: data['anesthesiaFee'],
            30165: data['coagulationFactorProductFee'],
            30166: data['cytokineProductFee'],
            30167: None,  # 无
            30168: data['inspectionDisposableMedicalMaterialsFee'],
            30169: data['disposableMedicalMaterialFeeForTreatment'],
            30170: data['disposableMedicalMaterialsForSurgery'],
            30171: data['otherFees']
        }
        return [fee]

    def get_yizhu(self, doc):
        url = self.host + '/app-nurse-station/patient/medical/record/order'
        json_data = {"inHospitalPatientId": doc['inhospitalPatientId'], "masterPatientIndex": doc['masterPatientIndex'],
                     "orderType": "1", "openingType": 0,
                     "orderCategoryList": ["1", "2", "3", "4", "5", "6", "7", "8"], }

        response = requests.post(url, headers=self.authorize, json=json_data)
        source_data = response.json()
        data = source_data['body']

        yizhu, koufu, zhenji = [], [], []
        for item in data:
            yizhu.append({
                30301: item['exeTime'],
                30302: item['orderText'],
                30303: item['stopTime']
            })

            nurse_content = item['usageName']
            if nurse_content and '口服' in nurse_content:
                koufu.append({
                    30501: item['exeTime'],
                    30502: item['orderName'],
                    30503: item['specification'],
                    30504: item['onceDosage'],
                    30505: item['frequencyName'],
                    30506: item['usageName'],
                    30507: item['totalNumUnit'],
                    30508: 3,
                    30509: item['stopTime']
                })
            if '注' in item['orderText'] or '针' in item['orderText']:
                zhenji.append({
                    30601: item['exeTime'],
                    30602: item['orderName'],
                    30603: item['specification'],
                    30604: item['onceDosage'],
                    30605: item['frequencyName'],
                    30606: item['usageName'],
                    30607: item['totalNumUnit'],
                    30608: 3,
                    30609: item['stopTime']
                })
        return yizhu, koufu, zhenji

    def get_blbg(self, doc):
        url = self.host + '/app-sys-manage/personality/table/getStyle/8947/1581667331'
        response = requests.post(url, headers=self.authorize)
        if response.json()['body']:
            logger.info(response.json()['body'])
            # assert None

    def get_xueyansuo(self, blh):
        from zhuyuan import xueyansuo
        xueyansuo = xueyansuo(blh)
        return xueyansuo

    def start(self):
        patient_name = self.source_info[3]
        blh = self.source_info[1]
        record_by_name = self.search_patient(patient_name)
        record_by_blh = self.search_patient(blh)
        records = quchong(record_by_name + record_by_blh)

        binganshouye = []
        yizhu_s, zhenji_s, koufu_s = [], [], []
        for item in records:
            patientinfo, checked_id = self.check_patient(item)
            if checked_id:
                patientinfo.update({
                    'diagnose': self.get_diagnoses(item, checked_id),
                    'operation': self.get_operation(item, checked_id),
                    'fee': self.get_fee(item)
                })
                binganshouye.append(patientinfo)
                yizhu, koufu, zhenji = self.get_yizhu(item)
                yizhu_s.extend(yizhu)
                koufu_s.extend(koufu)
                zhenji_s.extend(zhenji)
                self.get_blbg(item)
        xueyansuo = self.get_xueyansuo(blh)

        result = {
            'binganshouye': binganshouye,
            # 'gerenbingshi': '',  # hebingdao gerenbingshi
            'changqiyizhu': yizhu_s,
            'xysszbbg': xueyansuo,
            'cqkfyy': koufu_s,
            'cqzjyy': zhenji_s,
        }
        return result


if __name__ == '__main__':
    login()
    args = ('330106197504042418', '04386749', '', '杨一军', '1975-04-04')
    instance = NewHis(args)
    instance.start()
