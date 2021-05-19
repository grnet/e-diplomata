"""
ElGamal Backend
"""

from Cryptodome.Signature import DSS
from Cryptodome.PublicKey.ECC import EccPoint
from Cryptodome.Math.Numbers import Integer
from Cryptodome.PublicKey import ECC
from Cryptodome.Hash import SHA384
from util import *


def gen_curve(name):
    """
    Elliptic-curve generation
    """
    return ECC._curves[name]

def hash_into_scalar(bytes_seq, endianness='big'):
    """
    t -> H(t), where H(t) can act as scalar on elliptic points
    """
    value = int.from_bytes(SHA384.new(bytes_seq).digest(), endianness)
    return Integer(value)

def fiat_shamir(*points):
    """
    Fiat-Shamir heuristic over elliptic curve points
    """
    payload = ' '.join(map(lambda p: f'{p.xy}', points)).encode('utf-8')
    out = hash_into_scalar(payload)
    return out

def _ecc_pub(ecc_key):
    """
    Public part of provided key
    """
    return ecc_key.pointQ


class ElGamalCrypto(object):
    """
    The cryptosystem
    """

    def __init__(self, curve='P-384'):
        self.curve = gen_curve(name=curve)

    @property
    def generator(self):
        return self.curve.G

    @property
    def order(self):
        return self.curve.order

    
    # Serialization/Deserialization

    def serialize_ecc_point(self, pt):
        return [int(_) for _ in pt.xy]
    
    def deserialize_ecc_point(self, pt):
        return EccPoint(*pt, curve=self.curve.desc)
 
    def serialize_scalar(self, scalar):
        return int(scalar)
    
    def deserialize_scalar(self, scalar):
        return Integer(scalar)

    def serialize_ecc_key(self, ecc_key):
        pub  = self.serialize_ecc_point(ecc_key.pointQ)
        priv = self.serialize_scalar(ecc_key.d)
        return {
            'x': pub[0],
            'y': pub[1],
            'd': priv,
        }

    def deserialize_ecc_key(self, ecc_key):
        payload = {
            'curve': self.curve.desc,
            'point_x': ecc_key['x'],
            'point_y': ecc_key['y'],
            'd': ecc_key['d'],
        }
        return ECC.construct(**payload)

    def serialize_ecc_public(self, pub):
        return self.serialize_ecc_point(pub)

    def deserialize_ecc_public(self, pub):
        return self.deserialize_ecc_point(pub)

    def serialize_cipher(self, cipher):
        c1, c2 = extract_cipher(cipher)
        c1 = self.serialize_ecc_point(c1)
        c2 = self.serialize_ecc_point(c2)
        cipher = set_cipher(c1, c2)
        return cipher

    def deserialize_cipher(self, cipher):
        c1, c2 = extract_cipher(cipher)
        c1 = self.deserialize_ecc_point(c1)
        c2 = self.deserialize_ecc_point(c2)
        cipher = set_cipher(c1, c2)
        return cipher

    def serialize_ddh(self, ddh):
        return list(map(self.serialize_ecc_point, ddh))
    
    def deserialize_ddh(self, ddh):
        return tuple(map(
            self.deserialize_ecc_point, 
            ddh
        ))

    def serialize_chaum_pedersen(self, proof):
        u_comm, v_comm, s, d = extract_chaum_pedersen(proof)
        u_comm = self.serialize_ecc_point(u_comm)
        v_comm = self.serialize_ecc_point(v_comm)
        s = self.serialize_scalar(s)
        d = self.serialize_ecc_point(d)
        proof = set_chaum_pedersen(u_comm, v_comm, s, d)
        return proof
    
    def deserialize_chaum_pedersen(self, proof):
        u_comm, v_comm, s, d = extract_chaum_pedersen(proof)
        u_comm = self.deserialize_ecc_point(u_comm)
        v_comm = self.deserialize_ecc_point(v_comm)
        s = self.deserialize_scalar(s)
        d = self.deserialize_ecc_point(d)
        proof = set_chaum_pedersen(u_comm, v_comm, s, d)
        return proof
    
    def serialize_ddh_proof(self, ddh_proof):
        ddh, proof = extract_ddh_proof(ddh_proof)
        ddh = self.serialize_ddh(ddh)
        proof = self.serialize_chaum_pedersen(proof)
        ddh_proof = set_ddh_proof(ddh, proof)
        return ddh_proof
    
    def deserialize_ddh_proof(self, ddh_proof):
        ddh, proof = extract_ddh_proof(ddh_proof)
        ddh = self.deserialize_ddh(ddh)
        proof = self.deserialize_chaum_pedersen(proof)
        ddh_proof = set_ddh_proof(ddh, proof)
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
        g = self.generator                  # g
        r = self.generate_randomness()      # r
        cipher = set_cipher(
            r * g,
            m * g + r * pub,
        )                                   # r * g, m * g + r * y
        return cipher, r

    def decrypt(self, priv, cipher, table):
        a, b = extract_cipher(cipher)
        v = b + priv * (-a)
        return table[(str(v.x), str(v.y))]

    def reencrypt(self, public, cipher):    
        g = self.generator                  # g
        r = self.generate_randomness()      # r
        c1, c2 = extract_cipher(cipher)     # r_1 * g, m * g + r_1 * y
        cipher = set_cipher(
            r * g + c1,                     
            c2 + r * public,
        )                                   # (r1 + r2) * g, m * g + (r1 + r2) * y
        return cipher, r
    
    def drenc(self, cipher, decryptor):
        _, c2 = extract_cipher(cipher)
        m = c2 + (-decryptor)
        return m


    # Chaum-Pedersen protocol

    def generate_chaum_pedersen(self, ddh, z, *extras):
        g = self.generator
        p = self.order
        r = self.generate_randomness()
    
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


class Signer(object):
    """
    DSA (Digital Signature Algorithm) infrastructure
    """

    def __init__(self, key):
        self._signer = DSS.new(key, 'fips-186-3')
    
    def sign(self, payload):
        hc = SHA384.new(payload)
        signature = self._signer.sign(hc)
        return signature

    def verify_signature(self, s):
        raise NotImplementedError


class ElGamalSerializer(object):
    """
    Serializer infrastructure for wrapping ElGamal cryptosystems
    """

    def _serialize_ecc_point(self, pt):
        return self._cryptosys.serialize_ecc_point(pt)
    
    def _deserialize_ecc_point(self, pt):
        return self._cryptosys.deserialize_ecc_point(pt)
    
    def _serialize_scalar(self, scalar):
        return self._cryptosys.serialize_scalar(scalar)
    
    def _deserialize_scalar(self, scalar):
        return self._cryptosys.deserialize_scalar(scalar)

    def _serialize_ecc_key(self, ecc_key):
        return self._cryptosys.serialize_ecc_key(ecc_key)
    
    def _deserialize_ecc_key(self, ecc_key):
        return self._cryptosys.deserialize_ecc_key(ecc_key)

    def _serialize_ecc_public(self, pub):
        return self._cryptosys.serialize_ecc_public(pub)

    def _deserialize_ecc_public(self, pub):
        return self._cryptosys.deserialize_ecc_public(pub)

    def _serialize_cipher(self, cipher):
        return self._cryptosys.serialize_cipher(cipher)
    
    def _deserialize_cipher(self, cipher):
        return self._cryptosys.deserialize_cipher(cipher)

    def _serialize_ddh(self, ddh):
        return self._cryptosys.serialize_ddh(ddh)
    
    def _deserialize_ddh(self, ddh):
        return self._cryptosys.deserialize_ddh(ddh)

    def _serialize_chaum_pedersen(self, proof):
        return self._cryptosys.serialize_chaum_pedersen(proof)
    
    def _deserialize_chaum_pedersen(self, proof):
        return self._cryptosys.deserialize_chaum_pedersen(proof)
    
    def _serialize_ddh_proof(self, ddh_proof):
        return self._cryptosys.serialize_ddh_proof(ddh_proof)
    
    def _deserialize_ddh_proof(self, ddh_proof):
        return self._cryptosys.deserialize_ddh_proof(ddh_proof)
