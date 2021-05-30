"""
ElGamal Backend
"""

from Cryptodome.Signature import DSS
from Cryptodome.PublicKey.ECC import EccPoint
from Cryptodome.Math.Numbers import Integer
from Cryptodome.PublicKey import ECC
from Cryptodome.Hash import SHA384
from diplomata.util import *


def hash_into_scalar(bytes_seq, endianness='big'):
    value = int.from_bytes(SHA384.new(bytes_seq).digest(), endianness)
    return Integer(value)

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
        return Integer.random_range(
            min_inclusive=1, 
            max_exclusive=self.order
        )

    def ecc_point_from_scalar(self, scalar):
        return scalar * self.generator

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

    def reencrypt(self, public, cipher):    
        g = self.generator                  # g
        r = self.random_scalar()            # r
        c1, c2 = extract_cipher(cipher)     # r_1 * g, m + r_1 * y
        cipher = set_cipher(
            r * g + c1,                     
            c2 + r * public,
        )                                   # (r1 + r2) * g, m + (r1 + r2) * y
        return cipher, r
    
    def drenc(self, cipher, decryptor):
        _, c2 = extract_cipher(cipher)
        m = c2 + (-decryptor)
        return m

    def generate_chaum_pedersen(self, ddh, z, *extras):
        g = self.generator
        p = self.order
        r = self.random_scalar()
    
        u, v, w = ddh
        u_comm = r * u                                      # u commitment
        v_comm = r * g                                      # g commitment
    
        c = fiat_shamir(u, v, w, u_comm, v_comm, *extras)   # challenge
    
        s = (r + z * c) % p                                 # response
        d = z * u
    
        proof = set_chaum_pedersen(u_comm, v_comm, s, d)
        return proof
    
    def verify_chaum_pedersen(self, ddh, proof, *extras):
        g = self.generator
        u, v, w = ddh
        u_comm, v_comm, s, d = extract_chaum_pedersen(proof)
        c = fiat_shamir(u, v, w, u_comm, v_comm, *extras)   # challenge
        return (s * u == u_comm + c * d) and \
               (s * g == v_comm + c * v)

    def sign(self, key, message):
        signer = DSS.new(key, 'fips-186-3')
        hmsg = SHA384.new(message)
        signature = signer.sign(hmsg)
        return signature

    def verify_signature(self, sig, pub, message):
        verifier = DSS.new(pub, 'fips-186-3')
        hmsg = SHA384.new(message)
        try:
            verifier.verify(hmsg, sig)
        except ValueError:
            return False
        return True
