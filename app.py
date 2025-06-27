import hashlib
import json
import os
from datetime import datetime

import AES
import check
from RSA import RSAcode


def saveASE(data):
    os.makedirs("AESdata", exist_ok=True)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_path = os.path.join("AESdata", f"{current_time}.json")

    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print("已成功保存")


def saveRSA(data):
    os.makedirs("RSAdata", exist_ok=True)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_path = os.path.join("RSAdata", f"{current_time}.json")

    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print("已成功保存")


def findAES(username):
    # 遍历目标文件夹中的所有文件
    res = []
    for file_name in os.listdir('AESdata'):
        # 检查文件是否为 JSON 文件
        if file_name.endswith('.json'):
            # 构建文件的完整路径
            file_path = os.path.join('AESdata', file_name)
            # 读取 JSON 文件并转换为字典
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                if data['username'] == username:
                    res.append(data)
                # 输出文件名和读取的字典内容
                print(f"文件: {file_name}")
                print(f"内容: {data}")
                print()  # 空行分隔不同文件的输出
    return res


def findRSA(username):
    # 遍历目标文件夹中的所有文件
    res = []
    for file_name in os.listdir('RSAdata'):
        # 检查文件是否为 JSON 文件
        if file_name.endswith('.json'):
            # 构建文件的完整路径
            file_path = os.path.join('RSAdata', file_name)
            # 读取 JSON 文件并转换为字典
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                if data['username'] == username:
                    res.append(data)
                # 输出文件名和读取的字典内容
                print(f"文件: {file_name}")
                print(f"内容: {data}")
                print()  # 空行分隔不同文件的输出
    return res


def log_in():
    print("用户名：")
    return input()


def create_aes():
    print("您希望：A.自定义密钥 B.系统生成")
    option = input()
    flag = 0
    while not flag:
        key = ''
        if option == 'A':
            print("您创建的 AES 密钥：")
            key = input()
        else:
            key = AES.generate_strong_aes_key()
            print("系统生成的 AES 密钥: ", key)
        info = check.is_secure_aes_key(key)
        print(info[1])
        flag = info[0]
        print(AES.encode(key))
        key = AES.encode(key)

    sha256_hash = hashlib.sha256(key.encode()).hexdigest()

    print("设置您的 RSA 签名密钥：")
    print("p: ", end="")
    p = int(input())
    print("q: ", end="")
    q = int(input())
    a = RSAcode(p, q)

    now = a.encrypt_by_d(sha256_hash)
    data = {
        "username": username,
        "key": key,
        "signature": now
    }

    saveASE(data)


def view_aes():
    its = findAES(username)
    print("您的 RSA 签名公钥：")
    print("n: ", end="")
    n = int(input())
    a = RSAcode()
    a.M = n
    for c in its:
        now = AES.decode(c['key'])
        cur = a.decrypt_by_e(c['signature'])
        tag = hashlib.sha256(c['key'].encode()).hexdigest()
        if tag == cur:
            print('验证正确')
            print('密钥是：', now)
        else:
            print('验证错误，信息被篡改！')


def create_rsa():
    print("您希望：A.自定义密钥 B.系统生成")
    option = input()
    flag = 0
    while not flag:
        p, q, e = 0, 0, 0
        if option == 'A':
            print("您创建的 RSA 密钥：")
            print("p: ", end="")
            p = int(input())
            print("q: ", end="")
            q = int(input())
            print("您创建的 RSA 公钥：")
            print("e: ", end="")
            e = int(input())
        else:
            print('系统生成的 RSA 密钥：')
            tmp = RSAcode()
            tmp.rand()
            print("p: ", end="")
            print(tmp.p)
            print("q: ", end="")
            print(tmp.q)
            print("系统生成的 RSA 公钥：")
            print("e: ", end="")
            print(tmp.e)
        a = RSAcode(p, q)
        a.reload(e)
        info = check.check_rsa_safety(a)
        print(info[1])
        flag = info[0]

    dp = AES.encode(p)
    dq = AES.encode(q)

    sha256_hashp = hashlib.sha256(dp.encode()).hexdigest()
    sha256_hashq = hashlib.sha256(dq.encode()).hexdigest()

    print("设置您的 RSA 签名密钥：")
    print("p: ", end="")
    p = int(input())
    print("q: ", end="")
    q = int(input())
    a = RSAcode(p, q)

    # a = RSAcode(1610612741, 1061067769)
    # a.reload(65537)

    now = a.encrypt_by_d(sha256_hashp)
    cur = a.encrypt_by_d(sha256_hashq)
    data = {
        "username": username,
        "p": dp,
        "q": dq,
        "e": e,
        "signaturep": now,
        "signatureq": cur
    }

    saveRSA(data)


def view_rsa():
    its = findRSA(username)
    print("您的 RSA 签名公钥：")
    print("n: ", end="")
    n = int(input())
    a = RSAcode()
    a.M = n
    for c in its:
        now = a.decrypt_by_e(c['signaturep'])
        cur = a.encrypt_by_e(c['signatureq'])
        tag1 = hashlib.sha256(c['p'].encode()).hexdigest()
        tag2 = hashlib.sha256(c['q'].encode()).hexdigest()
        if tag1 == now and tag2 == cur:
            print('验证正确')
            print('密钥是：p = ', c['p'], end=", ")
            print("q = ", c['q'], end=", ")
            print('e = ', c['e'])
        else:
            print('验证错误，信息被篡改！')


username = log_in()

while True:
    print("您想要进行的操作：A.创建密钥 B.查看密钥 C.退出")
    choice1 = input()
    if choice1 == 'A':
        print("您想要创建的密钥：A.AES B.RSA")
        choice2 = input()
        if choice2 == 'A':
            create_aes()
        if choice2 == 'B':
            create_rsa()
    if choice1 == 'B':
        print("您想要查看的密钥：A.AES B.RSA")
        choice2 = input()
        if choice2 == 'A':
            view_aes()
        if choice2 == 'B':
            view_rsa()
    if choice1 == 'C':
        break
