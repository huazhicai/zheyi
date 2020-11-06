import pymongo

host = 'localhost'

client = pymongo.MongoClient(host)
db = client.hemodialysis
collection = db.BLOOD_Dialysis

for item in collection.find({"zhyl10000.zhyl10004": "吴永源"}):
    a = [i for i in item['zhyl90000'] if i['zhyl90004'] == 3]
    print(a)
    print(len(a))


db2 = client.config
collection2 = db2.hemo

for item in collection2.find({"yibanziliao.xingming": "吴永源"}):
    b = [i for i in item['zhenduanjilu'] if i['shujulaiyuan'] == 3]
    print(b)
    print(len(b))