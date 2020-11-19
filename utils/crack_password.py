import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5


# 安装
from utils.word import word


def crack_pwd(pwd):
    # 注意key的格式
    key = """-----BEGIN PUBLIC KEY-----        
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDXaFoMlA3ctUguD0rLbbFVqbajvlBH5jSWaZl7re + Xqp7BvoRwc5HOWGwtNvkUlv3WNIAw / YlUgWIz5r0fV6N8KHqSnV0CIpy7OJW67H1tVQ9Fbt4ZVx9RSJ378IBqN4ucacw2OuqA29I5AS9EhLCJWIXljPNNACmubPiv5mcn6wIDAQAB
    -----END PUBLIC KEY-----"""

    rsakey = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 生成对象
    cipher_text = base64.b64encode(cipher.encrypt(pwd.encode(encoding="utf-8")))  # 对传递进来的用户名或密码字符串加密
    value = cipher_text.decode('utf8')  # 将加密获取到的bytes类型密文解码成str类型
    return value


def crack_hospital(word):
    # 注意key的格式
    key = """-----BEGIN PUBLIC KEY-----        
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDXaFoMlA3ctUguD0rLbbFVqbajvlBH5jSWaZl7re + Xqp7BvoRwc5HOWGwtNvkUlv3WNIAw / YlUgWIz5r0fV6N8KHqSnV0CIpy7OJW67H1tVQ9Fbt4ZVx9RSJ378IBqN4ucacw2OuqA29I5AS9EhLCJWIXljPNNACmubPiv5mcn6wIDAQAB
    -----END PUBLIC KEY-----"""

    rsakey = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 生成对象
    cipher_text = base64.b64encode(cipher.decrypt(word.encode(encoding="utf-8")))  # 对传递进来的用户名或密码字符串加密
    value = cipher_text.decode('utf8')  # 将加密获取到的bytes类型密文解码成str类型
    return value

