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
def openssl_kdf(req):
    prev = ''
    while req > 0:
        prev = MD5.new(prev + secret + salt).digest()
        req -= 16
        yield prev


mat = ''.join([x for x in openssl_kdf(32 + 16)])
key = mat[0:32]
iv = mat[32:48]

dec = AES.new(key, AES.MODE_CBC, iv)
clear = dec.decrypt(data)

try:
    salt_hex = ''.join(["%X" % ord(c) for c in salt])
    print('salt:     %s' % salt_hex)
    print('expected: %s' % 'B898FE40EC8155FD')
    print('key:      %s' % hexlify(key).upper())
    print('expected: %s' % '4899E518743EB0584B0811AE559ED8AD9F0B5FA31B0B998FEB8453B8E3A7B36C')
    print('iv:       %s' % hexlify(iv).upper())
    print('expected: %s' % 'EFA6105F30F6C462B3D135725A6E1618')
    print('result:   %s' % clear)
except UnicodeDecodeError:
    print('decryption failed')
