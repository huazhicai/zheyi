`mongoexport -d futou -c merge_futou -o futou.json`
````

# 常规一个病人 26s


# 病人信息
POST http://his.zheyi.com/app-station-manage/medicalRecord/getInpatientInfo HTTP/1.1
{"inpatientId":124108,"masterPatientIndex":"c164f418542a4e18b67ad469296b34b2","medicalRecordDoctorId":null,"medicalRecordMasterId":"","type":2,"inpatientNo":""}

# 诊断
POST http://his.zheyi.com/app-station-manage/medicalRecord/getDiagnose HTTP/1.1
{"inpatientId":124108,"masterPatientIndex":"c164f418542a4e18b67ad469296b34b2","medicalRecordDoctorId":null,"medicalRecordMasterId":122361,"type":2,"inpatientNo":""}

# 手术
POST http://his.zheyi.com/app-station-manage/medicalRecord/getOperation HTTP/1.1
{"inpatientId":101138,"masterPatientIndex":"c164f418542a4e18b67ad469296b34b2","medicalRecordDoctorId":null,"medicalRecordMasterId":100073,"type":2,"inpatientNo":""}

# 费用
POST http://his.zheyi.com/app-hospitalized-register/recordSubject/detailAmountForRecordSubject HTTP/1.1
{"inhospitalPatientId":101138}

# 医嘱
POST http://his.zheyi.com/app-nurse-station/patient/medical/record/order HTTP/1.1
{"inHospitalPatientId":124108,"masterPatientIndex":"c164f418542a4e18b67ad469296b34b2","orderType":"1","openingType":0,"orderCategoryList":["1"],"orderSign":""}
orderCategoryList":["1","2","3","4","5","6","7","8"],"