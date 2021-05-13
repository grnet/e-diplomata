from Cryptodome.PublicKey import ECC
from Cryptodome.Signature import DSS
from Cryptodome.Hash import SHA384

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


# Commitments and signatures

def commit(curve, public, t):
    ht = hash_into_integer(t)                   # H(t)
    commitment, r = encrypt(curve, public, ht)  # (r * g, H(t) * g + r * I), r
    return commitment, r

# This is taken from https://github.com/kantuni/ZKP
def chaum_pedersen(curve, key, a, b):
    pub = ecc_pub_key(key)
    priv = int(key.d)
    r = random_factor(curve);
    u = a * r
    v = curve.G * r
    to_hash = f'{pub} {a} {b} {u} {v}'.encode('utf-8')
    h = hash_into_integer(to_hash)                      # challenge
    s = (r + h * priv) % curve.order                    # response
    d = a * priv
    return u, v, s, d

def serialize_chaum_pedersen(a, b, u, v, s, d):
    return {
        'a': [ int (z) for z in a.xy ],
        'b': [ int (z) for z in b.xy ],
        'u': [ int (z) for z in u.xy ],
        'v': [ int (z) for z in v.xy ],
        's': int(s),        
        'd': [ int (z) for z in d.xy ]
    }

def chaum_pedersen_verify(curve, pub, a, b, u, v, s, d):
    to_hash = f'{pub} {a} {b} {u} {v}'.encode('utf-8')
    h = hash_into_integer(to_hash)
    g = curve.G
    return (a * s == u + d * h) and (g * s == v + pub * h)
    
def make_table(g, n):
    table = {}
    for i in range(n):
        elem = (i * g)
        table[(str(elem.x), str(elem.y))] = i
    return table 
