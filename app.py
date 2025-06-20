from rsa import RSA
import check


secret = RSA()  # 创建一个实例

secret.rand(32)

check.check_rsa_safety (secret)

print('请输入明文：')

text = input()
encoded = secret.encode(text)
print("加密后：", encoded)

decoded = secret.decode(encoded)
print("解密后：", decoded)