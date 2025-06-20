from RSA import RSA
from AES import AES
import check


secret = RSA()  # 创建一个实例

secret.rand(32)

check.check_rsa_safety (secret)

print('请输入明文：')

text = input()
encoded = secret.encrypt(text)
print("加密后：", encoded)

decoded = secret.decrypt(encoded)
print("解密后：", decoded)

key = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
secret = AES(key)

plaintext = text
ciphertext = secret.encrypt(plaintext)
print(f"明文: {plaintext}")
print(f"密文: {ciphertext.hex()}")
print(f"解密: {secret.decrypt(ciphertext).decode()}")
