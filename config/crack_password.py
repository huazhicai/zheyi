import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
# 安装

def crack_pwd(pwd):
    key = """-----BEGIN PUBLIC KEY-----        
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDXaFoMlA3ctUguD0rLbbFVqbajvlBH5jSWaZl7re + Xqp7BvoRwc5HOWGwtNvkUlv3WNIAw / YlUgWIz5r0fV6N8KHqSnV0CIpy7OJW67H1tVQ9Fbt4ZVx9RSJ378IBqN4ucacw2OuqA29I5AS9EhLCJWIXljPNNACmubPiv5mcn6wIDAQAB
    -----END PUBLIC KEY-----"""  # 注意上述key的格式

    rsakey = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 生成对象
    cipher_text = base64.b64encode(cipher.encrypt(pwd.encode(encoding="utf-8")))  # 对传递进来的用户名或密码字符串加密
    value = cipher_text.decode('utf8')  # 将加密获取到的bytes类型密文解码成str类型
    return value


pwd = "123456"
# 亲测，这种方式加密密文的长度最多只能53个数字和英文字母。  这个跟公钥有关
# 全是中文只能加密17个
# encrypted = crack_pwd(pwd)
# print(encrypted)

