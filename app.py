from rsa import RSA


rsa = RSA()  # 创建一个实例

text = "Hello, RSA!"
encoded = rsa.encode(text)
print("加密后：", encoded)

decoded = rsa.decode(encoded)
print("解密后：", decoded)