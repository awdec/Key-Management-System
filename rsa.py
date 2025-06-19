class RSA:
    def __init__(self, p=None, q=None):
        # 默认使用给定的两个大素数
        self.p = p if p else int(1e9 + 7)
        self.q = q if q else 998244353
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

    def encode(self, s):
        t = []
        for c in s:
            now = ord(c)
            cur = pow(now, self.e, self.M)
            t.append(str(cur))
        return ','.join(t)

    def decode(self, s):
        a = list(map(int, s.split(',')))
        t = ''
        for now in a:
            cur = pow(now, self.d, self.M)
            t += chr(cur)
        return t
