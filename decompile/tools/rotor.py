"""Pure-Python port of CPython 2.x Modules/rotormodule.c (Enigma-style rotor cipher).

NeoX (NetEase) encrypts script.npk entries with it. C integer semantics (short
truncation, division toward zero) are emulated exactly.
"""
import math


def _cdiv(a, b):
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b >= 0) else -q


def _cmod(a, b):
    return a - b * _cdiv(a, b)


def _short(v):
    v &= 0xFFFF
    return v - 0x10000 if v & 0x8000 else v


class Rotor:
    def __init__(self, key, num_rotors=6):
        if isinstance(key, str):
            key = key.encode("latin-1")
        k1, k2, k3, k4, k5 = 995, 576, 767, 671, 463
        for ki in key:
            k1 = (((k1 << 3 | k1 >> 13) + ki) & 65535)
            k2 = (((k2 << 3 | k2 >> 13) ^ ki) & 65535)
            k3 = (((k3 << 3 | k3 >> 13) - ki) & 65535)
            k4 = ((ki - (k4 << 3 | k4 >> 13)) & 65535)
            k5 = (((k5 << 3 | k5 >> 13) ^ (~ki & 0xFFFFFFFF)) & 65535)
        self.key = [_short(k1), _short(k2 | 1), _short(k3), _short(k4), _short(k5)]
        self.rotors = num_rotors
        self.size = 256
        self._init()

    def _random(self):
        x, y, z = self.seed
        x = 171 * _cmod(x, 177) - 2 * _cdiv(x, 177)
        y = 172 * _cmod(y, 176) - 35 * _cdiv(y, 176)
        z = 170 * _cmod(z, 178) - 63 * _cdiv(z, 178)
        if x < 0:
            x += 30269
        if y < 0:
            y += 30307
        if z < 0:
            z += 30323
        self.seed = [x, y, z]
        term = x / 30269.0 + y / 30307.0 + z / 30323.0
        val = term - math.floor(term)
        return 0.0 if val >= 1.0 else val

    def _rand(self, s):
        return _cmod(_short(int(self._random() * s)), s)

    def _init(self):
        n, size = self.rotors, self.size
        self.seed = list(self.key[:3])
        self.pos = [1] * n
        self.adv = [1] * n
        self.e = [list(range(size)) for _ in range(n)]
        self.d = [list(range(size)) for _ in range(n)]
        for i in range(n):
            self.pos[i] = self._rand(size) & 0xFF
            self.adv[i] = (1 + 2 * self._rand(size // 2)) & 0xFF
            e, d = self.e[i], self.d[i]
            e[:] = range(size)
            k = size
            while k >= 2:
                q = self._rand(k)
                k -= 1
                j = e[q]
                e[q] = e[k]
                e[k] = j
                d[j] = k
            d[e[0]] = 0

    def _advance(self):
        n, size = self.rotors, self.size
        for i in range(n):
            t = self.pos[i] + self.adv[i]
            self.pos[i] = t % size
            if t >= size and i < n - 1:
                self.pos[i + 1] = (self.pos[i + 1] + 1) & 0xFF

    def decrypt(self, data):
        self._init()
        out = bytearray(len(data))
        n = self.rotors
        e_rng = range(n - 1, -1, -1)
        for idx, c in enumerate(data):
            for i in e_rng:
                c = (self.pos[i] ^ self.d[i][c]) & 0xFF
            out[idx] = c
            self._advance()
        return bytes(out)

    def encrypt(self, data):
        self._init()
        out = bytearray(len(data))
        for idx, p in enumerate(data):
            for i in range(self.rotors):
                p = self.e[i][(self.pos[i] ^ p) % self.size]
            out[idx] = p
            self._advance()
        return bytes(out)


# Key used by NeoX script.npk (public: neox_tools / nxs unpackers)
_dn, _dt, _df = "j2h56ogodh3se", "=dziaq.", '|os=5v7!"-234'
NEOX_KEY = _dn * 4 + (_dt + _dn + _df) * 5 + "!" + "#" + _dt * 7 + _df * 2 + "*" + "&" + "'"
