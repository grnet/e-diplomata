"""
ElGamal Backend
"""

from Cryptodome.PublicKey.ECC import EccPoint
from Cryptodome.Math.Numbers import Integer
from Cryptodome.PublicKey import ECC
from Cryptodome.Hash import SHA384
from diplomata.util import *


def hash_into_scalar(payload, endianness='big'):
    value = int.from_bytes(SHA384.new(payload).digest(), endianness)
    out = Integer(value)
    return out

def fiat_shamir(*points):
    payload = ' '.join(map(lambda p: f'{p.xy}', points)).encode('utf-8')
    out = hash_into_scalar(payload)
    return out

def _ecc_pub(ecc_key):
    return ecc_key.pointQ


class ElGamalCrypto(object):

    def __init__(self, curve='P-384'):
        self.curve = gen_curve(name=curve)

    @property
    def generator(self):
        return self.curve.G

    @property
    def order(self):
        return self.curve.order

    def random_scalar(self):
        rand = Integer.random_range(
            min_inclusive=1, 
            max_exclusive=self.order
        )
        return rand

    def hash_into_element(self, payload):
        g = self.generator
        s = hash_into_scalar(payload)
        return s * g

    def generate_key(self, curve='P-384'):
        return ECC.generate(curve=curve)
    
    def encrypt(self, pub, m):
        g = self.generator                  # g
        r = self.random_scalar()            # r
        cipher = set_cipher(
            r * g,
            m + r * pub,
        )                                   # r * g, m + r * y
        return cipher, r

    def decrypt(self, priv, cipher):
        a, b = extract_cipher(cipher)
        m = -(a * priv) + b
        return m

    def reencrypt(self, pub, cipher):    
        g = self.generator                  # g
        r = self.random_scalar()            # r
        c1, c2 = extract_cipher(cipher)     # r_1 * g, m + r_1 * y
        cipher = set_cipher(
            r * g + c1,                     
            c2 + r * pub,
        )                                   # (r1 + r2) * g, m + (r1 + r2) * y
        return cipher, r

    def create_decryptor(self, r, pub):
        return r * pub                      # r * y = r * x * g
    
    def decrypt_with_decryptor(self, cipher, decryptor):
        _, c2 = extract_cipher(cipher)
        m = c2 + (-decryptor)
        return m

    def generate_chaum_pedersen(self, ddh, z, *extras):
        g = self.generator
        p = self.order

        u, v, w = ddh

        r = self.random_scalar()

        g_comm = r * g
        u_comm = r * u

        challenge = fiat_shamir(u, v, w, g_comm, u_comm, *extras)
        response = (r + z * challenge) % p

        proof = set_chaum_pedersen(g_comm, u_comm, challenge, response)
        return proof
    
    def verify_chaum_pedersen(self, ddh, proof, *extras):
        g = self.generator

        u, v, w = ddh
        g_comm, u_comm, challenge, response = extract_chaum_pedersen(proof)

        return all((
            challenge == fiat_shamir(u, v, w, g_comm, u_comm, *extras),
            response * g == g_comm + challenge * v,
            response * u == u_comm + challenge * w,
        ))
