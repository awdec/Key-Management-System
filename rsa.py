from sympy import randprime


class RSA:
    def __init__(self, p=None, q=None):
        # 默认使用给定的两个大素数
        self.p = p if p else int(1e9 + 7)
        self.q = q if q else 998244353
        self.M = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = self.phi - 1  # e 选为 phi - 1
        self.d = self.inv(self.e, self.phi)

    def generate_large_prime(self, bits=512):
        """生成一个指定比特长度的随机质数"""
        low = 1 << (bits - 1)  # 最小值：2^(bits-1)
        high = (1 << bits) - 1  # 最大值：2^bits - 1
        return randprime(low, high)

    def rand(self, bits=512):
        self.p = self.generate_large_prime(bits)
        self.q = self.generate_large_prime(bits)
        while self.q == self.p:  # 确保 p ≠ q
            self.q = self.generate_large_prime(bits)
        self.M = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = self.phi - 1  # e 选为 phi - 1
        self.d = self.inv(self.e, self.phi)

    def exgcd(self, a, b):
        if b == 0:
            return 1, 0
        else:
            x, y = self.exgcd(b, a % b)
            return y, x - (a // b) * y

    def inv(self, a, mod):
        x, _ = self.exgcd(a, mod)
        return (x % mod + mod) % mod

    def encrypt(self, s):
        t = []
        for c in s:
            now = ord(c)
            cur = pow(now, self.e, self.M)
            t.append(str(cur))
        return ','.join(t)

    def decrypt(self, s):
        a = list(map(int, s.split(',')))
        t = ''
        for now in a:
            cur = pow(now, self.d, self.M)
            t += chr(cur)
        return t
