import json
from base64 import b64decode, b64encode
from binascii import hexlify
from Crypto.Cipher import AES
from Crypto.Hash import MD5

secret = 'secret'
encoded = 'U2FsdGVkX1+4mP5A7IFV/VcgRs4ci/yupMErHjf5bkT5XrcowXK7z3VyyV1l2jvy'
encrypted = b64decode(encoded)
salt = encrypted[8:16]
data = encrypted[16:]

# We need 32 bytes for the AES key, and 16 bytes for the IV
with open('zhusu.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

id = []
xuyao = []
for i in data['body']:
    ids = i['fileUniqueId']
    if ids in id:
        xuyao.append(ids)
    id.append(ids)

print(xuyao)

json_data = {
    'patientId': '222968',
    'visitId': '2',
    'deptCode': '12472',
    'fileVisitType': '2',
    'appClass': 'INPAT_DOCT',
    'patientRegisterId': '222968',
    'masterPatientIndex': 'b92cde680ffb4bd5a02456dd474b188c',
    'orgId': '1',
    'inhospitalPatientId': '139282',
    'outpatientId': '-1',
    'patientName': '相樟生',
    'bedLabel': '7',
    'bedNo': '7',

}
