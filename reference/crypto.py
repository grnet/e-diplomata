"""
Crypto layer (El-Gamal)
"""

from util import *


class ElGamalCrypto(object):

    def __init__(self, curve='P-384'):
        self.curve = gen_curve(curve)

    @property
    def generator(self):
        return self.curve.G

    @property
    def order(self):
        return self.curve.order

    
    # Structures

    def serialize_ecc_point(self, pt):
        return [int(_) for _ in pt.xy]
    
    def deserialize_ecc_point(self, pt):
        return EccPoint(*pt, curve=self.curve.desc)
    
    def serialize_factor(self, factor):
        return int(factor)
    
    def deserialize_factor(self, factor):
        return Integer(factor)

    def set_cipher(self, c1, c2):
        cipher = {
            'c1': c1,
            'c2': c2,
        }
        return cipher
    
    def extract_cipher(self, cipher):
        c1 = cipher['c1']
        c2 = cipher['c2']
        return c1, c2

    def serialize_ddh(self, ddh):
        return list(map(self.serialize_ecc_point, ddh))
    
    def deserialize_ddh(self, ddh):
        return tuple(map(
            self.deserialize_ecc_point, 
            ddh
        ))

    def set_proof(self, u_comm, v_comm, s, d):
        return {
            'u_comm': u_comm,
            'v_comm': v_comm,
            's': s,
            'd': d,
        }

    def extract_proof(self, proof):
        u_comm = proof['u_comm']
        v_comm = proof['v_comm']
        s = proof['s']
        d = proof['d']
        return u_comm, v_comm, s, d

    def serialize_proof(self, proof):
        u_comm, v_comm, s, d = self.extract_proof(proof)
        u_comm = self.serialize_ecc_point(u_comm)
        v_comm = self.serialize_ecc_point(v_comm)
        s = self.serialize_factor(s)
        d = self.serialize_ecc_point(d)
        proof = self.set_proof(u_comm, v_comm, s, d)
        return proof
    
    def deserialize_proof(self, proof):
        u_comm, v_comm, s, d = self.extract_proof(proof)
        u_comm = self.deserialize_ecc_point(u_comm)
        v_comm = self.deserialize_ecc_point(v_comm)
        s = self.deserialize_factor(s)
        d = self.deserialize_ecc_point(d)
        proof = self.set_proof(u_comm, v_comm, s, d)
        return proof
    
    def set_ddh_proof(self, ddh, proof):
        return {
            'ddh': ddh,
            'proof': proof
        }
    
    def extract_ddh_proof(self, ddh_proof):
        ddh = ddh_proof['ddh']
        proof = ddh_proof['proof']
        return ddh, proof

    def serialize_ddh_proof(self, ddh_proof):
        ddh, proof = self.extract_ddh_proof(ddh_proof)
        ddh = self.serialize_ddh(ddh)
        proof = self.serialize_proof(proof)
        ddh_proof = self.set_ddh_proof(ddh, proof)
        return ddh_proof
    
    def deserialize_ddh_proof(self, ddh_proof):
        ddh, proof = self.extract_ddh_proof(ddh_proof)
        ddh = self.deserialize_ddh(ddh)
        proof = self.deserialize_proof(proof)
        ddh_proof = self.set_ddh_proof(ddh, proof)
        return ddh_proof


    # Generation

    def generate_randomness(self):
        return Integer.random_range(
            min_inclusive=1, 
            max_exclusive=self.order
        )

    def generate_key(self):
        return ECC.generate(curve=self.curve.desc)
    

    # Encryption/Decryption

    def encrypt(self, pub, m):
        g = self.generator
        r = self.generate_randomness()
        cipher = self.set_cipher(
            r * g,
            m * g + r * pub,
        )
        return cipher, r

    def decrypt(self, priv, cipher, table):
        a, b = self.extract_cipher(cipher)
        v = b + priv * (-a)
        return table[(str(v.x), str(v.y))]

    def reencrypt(self, public, cipher):    
        g = self.generator
        r = self.generate_randomness()
        c1, c2 = self.extract_cipher(cipher)
        cipher = self.set_cipher(
            r * g + c1,
            c2 + r * public,
        )
        return cipher, r
    
    def drenc(self, cipher, decryptor):
        _, c2 = self.extract_cipher(cipher)
        m = c2 + (-decryptor)
        return m


    # Chaum-Pedersen protocol

    def generate_chaum_pedersen(self, ddh, z, *extras):
        g = self.generator
        p = self.order
        r = self.generate_randomness()
    
        u, v, w = ddh
        z = int(z)
    
        u_comm = r * u                                      # u commitment
        v_comm = r * g                                      # g commitment
    
        c = fiat_shamir(u, v, w, u_comm, v_comm, *extras)   # challenge
    
        s = (r + z * c) % p                                 # response
        d = z * u
    
        proof = self.set_proof(u_comm, v_comm, s, d)
        return proof
    
    def verify_chaum_pedersen(self, ddh, proof, *extras):
        g = self.generator
        u, v, w = ddh
        u_comm, v_comm, s, d = self.extract_proof(proof)
        c = fiat_shamir(u, v, w, u_comm, v_comm, *extras)   # challenge
        return (s * u == u_comm + c * d) and \
               (s * g == v_comm + c * v)
