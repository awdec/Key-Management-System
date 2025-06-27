import math
from collections import Counter


def check_rsa_safety(rsa):
    n = rsa.p * rsa.q
    key_size = n.bit_length()
    e = rsa.e
    issues = []
    if key_size < 1024:
        issues.append("❌ 密钥太短，完全不安全（<1024 位）")
    elif key_size < 2048:
        issues.append("⚠️ 密钥较短，已不推荐使用（建议 ≥2048 位）")
    if e != 65537:
        issues.append(f"⚠️ 公钥指数为 {e}，建议使用 65537（安全高效）")
    if issues:
        return False, issues
    else:
        return True, "🎉 没有发现风险，密钥设置合理"


# 示例弱密钥列表（可扩展）
WEAK_KEYS = {
    b"1234567890123456",
    b"passwordpassword",
    b"letmeinletmein!!",
    b"adminadminadmin12",
    b"9876543210987654",
}


def check_aes_key_length(key: bytes) -> bool:
    print(len(key))
    return len(key) in [16, 24, 32]  # 128/192/256 位


def shannon_entropy(data: bytes) -> float:
    counter = Counter(data)
    total = len(data)
    entropy = -sum((count / total) * math.log2(count / total) for count in counter.values())
    return entropy


def is_weak_key(key: bytes) -> bool:
    return key in WEAK_KEYS


def is_secure_aes_key(key: bytes):
    # 检查密钥长度
    if not check_aes_key_length(key):
        return False, "❌ 无效的 AES 密钥长度，应为 16、24 或 32 字节"

    # 检查是否为常见弱密钥
    if is_weak_key(key):
        return False, "❌ 密钥在已知弱密钥列表中，容易被猜测"

    # 计算 Shannon 熵，检测随机性
    entropy = shannon_entropy(key)
    if entropy < 4.0:
        return False, f"❌ 密钥熵过低（{entropy:.2f}），随机性不足"

    return True, "✅ 密钥强度良好，可安全用于 AES 加密"


