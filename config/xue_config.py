# -*- coding: utf-8 -*-


# 血透数据库连接配置
host = '192.168.50.217'
port = 1433
user = 'sa'
password = 'Huamai521'
database = 'hemodialysis'
system_tag_id = 1


xuetou_id = [16497, 16351, 12933, 18816, 6629, 2432, 5670, 5521, 9567, 3058, 14865, 19889,
             8641, 14140, 7328, 17338, 22690, 18695, 21656, 8454, 13494, 7370, 3433, 17622,
             9766, 4564, 20332, 14278, 19989, 6555, 16226, 6188, 16379, 8625, 2603, 7558,
             15739, 19608, 22427, 16350, 371, 22530, 20614, 17638, 6003, 7426, 21412, 18252,
             139, 2484, 4896, 232, 11538, 18769, 6322, 20902, 4348, 13220, 5505, 20084, 15015,
             4377, 3893, 17402, 6041, 11713, 18783, 11205, 10953, 5822, 12778, 186, 13621, 5287,
             21983, 16411, 13764, 3050, 23587, 5464, 4699, 13185, 12557, 8760, 2062, 14442, 21901,
             2718, 16389, 10717, 8387, 1540, 3902, 6515, 22326, 5615, 9221, 2549, 2850, 11070,
             14202, 7774, 22684, 3740, 7902, 12721, 8225, 11396, 10481, 19845, 4905, 16935, 2280,
             13905, 1622, 14104, 10194, 23166, 12987, 6805, 18272, 18418, 23651, 5630, 19275, 9709,
             18030, 6806, 2592, 13511, 7786, 12193, 7916, 674, 22155, 6239, 3285, 16943, 20789, 15013,
             17034, 21921, 17744, 6762, 7687, 10322, 13423, 11506, 16881, 15825, 22676, 19918, 17461,
             13806, 21572, 21586, 10035, 19233, 9996, 20848, 7025, 6345, 22291, 15500, 5468, 11191,
             8990, 6691, 21519, 2891, 18780, 14126, 7855, 12108, 16909, 23272, 14000, 12324, 18808,
             5117, 15812, 13969, 7512, 2327, 22386, 8325, 20226, 20006, 21217, 12484, 2323, 16783, 12713,
             2006, 506, 13619, 1828, 15065, 11932, 8715, 7594, 7021]


xuetou_50 = [13969, 16351, 12933, 18816, 6629, 2432, 5670, 5521, 9567, 3058, 14865, 19889,
             8641, 14140, 17338, 22690, 18695, 21656, 8454, 13494, 7370, 3433, 17622,
             9766, 4564, 20332, 14278, 19989, 6555, 16226, 6188, 16379, 8625, 2603, 7558,
             15739, 19608, 22427, 16350, 371, 22530, 20614, 17638, 6003, 7426, 21412, 18252,
             139, 2484]

ybzl_sql = """select insure, MenZhenCode, ZhuyuanCode, Name, B.ItemName, IdentityCard, BirthDate, Nationality,
                   Marriage, Stature, Heft, Xiyan, Yinjiu, Shili, C.ItemName, FirstDialyseTime, Income_Time, D.ItemName,
                    E.ItemName, F.ItemName, workaddress, G.ItemName, Address, Telephone, MobilePhone,
                   H.ItemName, ZJXL, PJHZ, JBRS, YHJH, YWYL, JZZK, ZLZ, Patient.modify_time
                   from Patient left join DictionaryItem B on  Patient.Sex = B.ID
                  left join DictionaryItem C on  Patient.PaymentWay = C.ID
                  left join DictionaryItem D on  Patient.Province = D.ID
                  left join DictionaryItem E on  Patient.City = E.ID
                  left join DictionaryItem F on  Patient.District = F.ID
                  left join DictionaryItem G on  Patient.Occupation = G.ID
                  left join DictionaryItem H on  Patient.Culture = H.ID
                  where Patient.id={}"""
ybzl_keys = [10101, 10102, 10103, 10104, 10105, 10114, 10106, 10107, 10108,
             10109, 10110, 10111, 10112, 10113, 10115, 10116, 10117, 10118,
             10119, 10120, 10121, 10122, 10123, 10124, 10125, 10126, 10127,
             10128, 10129, 10130, 10131, 10132, 10133, 'modify_time']
sex_key = ybzl_keys[4]

bingshi_sql = """select A.DateTime, A.Shenyzshi, A.PDshi,substring(A.Zhusu,1,10000), substring(A.XianBshi,1,10000),
                substring(A.JiWshi,1,10000), A.GMyaow, B.Yingyangzhuangtai, B.TiWei, B.FuZhong, B.Fuzhongchengdu, B.Qita 
                from Bingshi A  left join Tijian B on A.tijianid=B.ID  where A.Patient_id ={}
                """
bingshi_keys = [10201, 10206, 10207, 10208, 10209, 10210, 10211, 10202, 10203, 10204, 10212, 10205]

xgtl_sql = """select A.SetupTime, A.StopTime, A.StopReason, A.VesselType,
                  B.ItemName, C.ItemName,  D.ItemName  
                  from DialyseRoute A left join DictionaryItem B on A.VesselRouteType = B.ID
                  left join DictionaryItem C on A.VesselRouteSort = C.ID
                  left join DictionaryItem D on A.vesselroutecztype = D.ID
                   where Patient_id ={}"""
xgtl_keys = [10301, 10306, 10307, 10304, 10302, 10303, 10305]

lshjl_sql = """select A.SetupTime, B.ItemName, A.DriedWeight, A.DiFrequency, D.ItemName, E.Name, C.DialyseTime, 
                        C.ReplaceFluidQTY from DialyseScheme A left join DictionaryItem B on A.HeparineType = B.ID
                        right join DialyseSchemeSub C on A.ID = C.Scheme_ID
                        left join DictionaryItem D on C.DialyseType = D.ID
                        left join DializerClass E on C.DialyzerClassID = E.ID
                        where Patient_id ={}"""
lshjl_keys = [10401, 10402, 10403, 10404, 10405, 10406, 10407, 10408]

crrtjl_sql = """select A.CRRTtime, B.CRRTjiqi, B.Daoguanxinghao, B.Zhiliaoshijian 
                  from CRRT A left join CRRTTouxifangan B on A.CRRTTouxifangan_id = B.ID 
                  where A.Patient_id ={}"""
crrtjl_keys = [11201, 11202, 11203, 11204]

hpjl_sql = """select A.HPtime,B.HPjiqi,B.Daoguanxinghao, B.Zhiliaoshijian 
                  from HP A left join HPTouxifangan B on A.HPTouxifangan_id = B.ID
                  where A.Patient_id ={}"""
hpjl_keys = [11301, 11302, 11303, 11304]

tpejl_sql = """select A.TPEtime,B.TPEjiqi,B.Daoguanxinghao, B.Zhiliaoshijian 
                  from TPE A left join TPETouxifangan B on A.TPETouxifangan_id = B.ID 
                  where A.Patient_id ={}"""
tpejl_keys = [11401, 11402, 11403, 11404]

dfppjl_sql = """select DFPPtime,DFPPjiqi, Daoguanxinghao, Zhiliaoshijian 
                  from DFPPRecord where Patient_id ={}"""
dfppjl_keys = [11501, 11502, 11503, 11504]

iajl_sql = """select IAtime,IAjiqi, Daoguanxinghao, Zhiliaoshijian 
                  from IARecord where Patient_id ={}"""
iajl_keys = [11601, 11602, 11603, 11604]

txjl_sql = """select SetupTime ,C.ItemName ,BMI, tqShousuoya,tqShuzhangya ,TQxinlv, 
                  TQHuxi ,Cexueyabuwei , Stime, Jingti, DialyseWeightLater,
                   RealDewater, D.ItemName, Zongzhyliang, thShousuoya,thShuzhangya , THxinlv ,THHuxi 
                  from DialyseRecord A left join DialyseSchemeSub B on A.SubDialyseScheme_ID=B.ID
                  left join DictionaryItem C on B.DialyseType = C.ID
                   left join DictionaryItem D on BloodRouteFlow=D.ID
                   where Patient_id={}"""
txjl_keys = [11101, 11102, 11105, 10501, 10502, 10503, 10504, 10505, 10506,
             10507, 10508, 10509, 10510, 10511, 10516, 10517, 10518, 10519]

zhgjl_sql = """select A.ChangeTime,B.itemName as ChangeStatus,C.itemName as ChangeMode
                  from OUTCOME A left join DictionaryItem B on A.ChangeStatus=B.ID
                  left join DictionaryItem C on A.ChangeMode=C.ID where Patient_id ={}"""
zhgjl_keys = [10601, 10602, 10603]

zhenduan_sql = """select DiagnoseTime,DefineName,B.itemName  
                  from Diagnose A left join DictionaryItem B on A.Property=B.ID 
                  where Patient_id ={}"""
zhenduan_keys = [10701, 10702, 10703]

shshjl_sql = """select OPS_Time, OPS_Cause, OPS_Type from OPSSchedule 
                  where Patient_id={}"""
shshjl_keys = [10801, 10802, 10803]

yizhu_sql = """select MedicineDate, MName, Amount, JiLiang, UMethod, MedicineWay 
                  from MedicineTreatment where Patient_id={}"""
yizhu_keys = ['kaiyaoshijian', 'yaowumingcheng', 'yicijiliang', 'danwei', 'yongyaopinlv', 'yongfa']

yyzpl_sql = 'select Setup_Time,Point,JieLun from ZungSDS where Patient_id={}'
yyzpl_keys = [11701, 11702, 11703]

jlzpl_sql = 'select Setup_Time,Point,JieLun from ZungSAS where Patient_id={}'
jlzpl_keys = [11801, 11802, 11803]

aisengkerenge_sql = """select Setup_Time, EL,NL,PL,ll,Point 
                            from EPQ where PaTIENT_ID={}"""
aisengkerenge_keys = [11901, 11902, 11903, 11904, 11905, 11906]

zhengzhuangziping_sql = """select Setup_Time, QuTiH,QiangPoZZ,RenJiGXMG,YiTu,JiaoLv, DiDui,KongJu,
                                     PianZhi,JingShenBX,QT,YangXingXMS,YinXingXMS, YangXingZZJF,ZongJunF,
                                    Point from SCL90 where PaTIENT_ID={}"""

zhengzhuangziping_keys = [12001, 12004, 12005, 12006, 12007, 12008, 12009, 12010,
                          12011, 12012, 12013, 12014, 12015, 12016, 12003, 12002]

lingwushehui_sql = 'select Setup_Time,JiaTingN,JiaTingW,Point from PSSS where PaTIENT_ID={}'
lingwushehui_keys = [12101, 12103, 12104, 12102]

zhgzhxyyzhkpg_sql = """select Create_Time, PF, JSZBH, JSSJ, JSLX, WeiChangD, GNYCZYC,
                      GNYC2Z, TJPXDJ, TJJRDJ,TJSZDJ,WLL, WLR from SGA where Patient_id={}"""
zhgzhxyyzhkpg_keys = [12201, 12202, 12203, 12204, 12205, 12206, 12207, 12208, 12209, 12210, 12211, 12212, 12213]

shhzhlwj_sql = """select Setup_Time ,Point ,ZhengZhuangYXPF, ShenBingYXPF ,ShenBingFDPF ,
                          GongZuoZTPF ,RenZhiGNPF ,SheHuiYXPF , XingGongNPF ,ShuiMianZLPF ,SheHuiZCLPF ,
                          YiHuRYZCDPF ,ZiWoJKPF , HuanZheMYDPF ,ShenTiGNPF ,SheHuiJSPF ,
                          TengTongDPF ,ZongTiZKPF , QingGanZKPF,SheHuiQGPF ,SheHuiGNPF ,JingLiTLPF
                          from KDQOL where Patient_id={}"""
shhzhlwj_keys = [12401, 12402, 12403, 12404, 12405, 12406, 12407, 12408, 12409, 12410, 12411,
                 12412, 12413, 12414, 12415, 12416, 12417, 12418, 12419, 12420, 12421, 12422]

pixiazhifan_sql = """select Setup_Time, ShangBiW,ShangBiJW, ErTouJ,SanTouJ,EGuSP,JianJXP
                               from PXZFCDPG where Patient_id={}"""
pixiazhifan_keys = [12501, 12502, 12503, 12504, 12505, 12506, 12507]

shwzkpg_sql = """select Setup_Time,CeDingSJD,ShouTXSWDYK,ECWTBW,TiZhiFang
                      from SWZKPG where Patient_id={}"""
shwzkpg_keys = [12601, 12602, 12603, 12604, 12605]

wolipinggu_sql = 'select create_time,WoLiZ,WoLiY from WoLiPG where Patient_id={}'
wolipinggu_keys = [12701, 12702, 12703]

qshqkpg_sql = """ select Setup_Time,YYZK,XXGGN,MXYZ,GLDX,WKQK,TXCFX
                          from QSQKPG where Patient_id={}"""
qshqkpg_keys = [12801, 12802, 12803, 12804, 12805, 12806, 12807]

siwang_sql = """select OutDate, Death_reason, Death_reasonsub1, Death_reasonsub2, Death_reasonsub3, 
                  Siqiantidai_fs, Siqianzhongzhi, Siqianzhiti_yy, Jieshoushen_yz, Zuihouyizhi_rq
                  from DeathRecord where Patient_id={}"""
siwang_keys = [12901, 12902, 12903, 12904, 12905, 12906, 12907, 12908, 12909, 12910]
