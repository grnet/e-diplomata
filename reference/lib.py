from Cryptodome.PublicKey import ECC
from Cryptodome.Signature import DSS
from Cryptodome.Hash import SHA384

from Cryptodome.PublicKey.ECC import EccPoint
from Cryptodome.Math.Numbers import Integer

import nacl.utils
from nacl.public import PrivateKey, Box

import json
import re


def hash_into_integer(bytes_seq, endianness='big'):
    """
    The t -> H(t) functionality of the deliverable
    """
    return int.from_bytes(SHA384.new(bytes_seq).digest(), endianness)

def random_factor(curve):
    """
    Plays the same role as random exponent
    in numerical ElGamal cryptosystems
    """
    return Integer.random_range(
        min_inclusive=1, 
        max_exclusive=curve.order
    )

def ecc_point_to_bytes(ecc_point):
    return ecc_point.x.to_bytes(), ecc_point.y.to_bytes()

def ecc_point_to_str(ecc_point):
    return ecc_point.x.to_bytes(), ecc_point.y.to_bytes()

def gen_curve(curve_name):
    curve = ECC._curves[curve_name]
    return curve

def ecc_pub_key(ecc_key):
    return ecc_key.pointQ


# ElGamal encryption/decryption

def set_cipher(alpha, beta):
    cipher = {
        'alpha': alpha,
        'beta': beta
    }
    return cipher

def extract_cipher(cipher):
    alpha = cipher['alpha']
    beta = cipher['beta']
    return alpha, beta
    
def encrypt(curve, public, m):
    g = curve.G
    r = random_factor(curve)
    cipher = set_cipher(
        r * g,
        m * g + r * public,
    )
    return cipher, r

def decrypt(key, cipher, table):
    a, b = extract_cipher(cipher)
    v = b + (key.d * (-a))
    return table[(str(v.x), str(v.y))]

def reencrypt(curve, public, cipher):    
    g = curve.G
    r = random_factor(curve)
    c1, c2 = extract_cipher(cipher)
    cipher = set_cipher(
        r * g + c1,
        c2 + r * public,
    )
    return cipher, r

def drenc(cipher, decryptor):
    _, c2 = extract_cipher(cipher)
    m = c2 + (-decryptor)
    return m


# Commitments

def commit(curve, public, t):
    ht = hash_into_integer(t)                   # H(t)
    commitment, r = encrypt(curve, public, ht)  # (r * g, H(t) * g + r * I), r
    return commitment, r

# Chaum-Pedersen

def fiat_shamir(*points):
    to_hash = ' '.join(map(lambda p: f'{p.xy}', points))
    output = hash_into_integer(to_hash.encode('utf-8'))
    return output

def chaum_pedersen(curve, ddh, z, *extras):
    """
    """
    g = curve.G
    r = random_factor(curve);

    u, v, w = ddh

    u_comm = r * u                                   # u commitment
    v_comm = r * g                                   # g commitment

    c = fiat_shamir(u, v, w, u_comm, v_comm, *extras)   # challenge

    s = (r + c * z) % curve.order                    # response
    d = z * u
    return u_comm, v_comm, s, d

def serialize_chaum_pedersen(u, v, u_comm, v_comm, s, d):
    return {
        'u': [ int (_) for _ in u.xy ],
        'v': [ int (_) for _ in v.xy ],
        'u_comm': [ int (_) for _ in u_comm.xy ],
        'v_comm': [ int (_) for _ in v_comm.xy ],
        's': int(s),        
        'd': [ int (_) for _ in d.xy ]
    }

def deserialize_chaum_pedersen(curve, proof):
    u = EccPoint(*proof['u'], curve=curve.desc)
    v = EccPoint(*proof['v'], curve=curve.desc)
    u_comm = EccPoint(*proof['u_comm'], curve=curve.desc)
    v_comm = EccPoint(*proof['v_comm'], curve=curve.desc)
    s = Integer(proof['s'])
    d = EccPoint(*proof['d'], curve=curve.desc)
    return u, v, u_comm, v_comm, s, d

def chaum_pedersen_verify(curve, ddh,
        u_comm, v_comm, s, d, *extras):
    g = curve.G
    u, v, w = ddh
    c = fiat_shamir(u, v, w, u_comm, v_comm,  *extras)   # challenge
    return (s * u == u_comm + c * d) and \
           (s * g == v_comm + c * v)
    
def make_table(g, n):
    table = {}
    for i in range(n):
        elem = (i * g)
        table[(str(elem.x), str(elem.y))] = i
    return table 
