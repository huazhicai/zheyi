import base64

from Cryptodome.Cipher import AES
# from Crypto.Cipher import AES


def add_to_16(text):
    while len(text) % 16 != 0:
        text += '\0'
    return (text)


key = 'Fcniggersm'
key = add_to_16(key)


def decode_base64(data):
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += '=' * missing_padding
    return (data)


message = 'gYknrv3zMWYXEpRLDL0n8q+6s68DKapAfRpBDhN1XGM='
encrypt_data = message
encrypt_data = decode_base64(encrypt_data)

cipher = AES.new(key, AES.MODE_CFB)
result2 = base64.b64decode(encrypt_data)
a = cipher.decrypt(result2)

a = a.decode('utf-8', 'ignore')
a = a.rstrip('\n')
a = a.rstrip('\t')
a = a.rstrip('\r')
a = a.replace('\x06', '')
print('\n', 'data:', a)
