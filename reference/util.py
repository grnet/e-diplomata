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

def fiat_shamir(*points):
    """
    Fiat-Shamir heuristic over elliptic curve points
    """
    # import pdb; pdb.set_trace()
    to_hash = ' '.join(map(lambda p: f'{p.xy}', points))
    output = hash_into_integer(to_hash.encode('utf-8'))
    return output

def random_factor(curve):
    """
    Plays the same role as random exponent in numerical ElGamal
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

def serialize_ecc_point(pt):
    return [int(_) for _ in pt.xy]

def deserialize_ecc_point(curve, pt):
    return EccPoint(*pt, curve=curve.desc)

def serialize_factor(factor):
    return int(factor)

def deserialize_factor(factor):
    return Integer(factor)


# Chaum-Pedersen

def serialize_ddh(ddh):
    return list(map(serialize_ecc_point, ddh))

def deserialize_ddh(curve, ddh):
    return tuple(map(lambda p: deserialize_ecc_point(curve, p), ddh))

def set_proof(u_comm, v_comm, s, d):
    return {
        'u_comm': u_comm,
        'v_comm': v_comm,
        's': s,
        'd': d,
    }

def extract_proof(proof):
    u_comm = proof['u_comm']
    v_comm = proof['v_comm']
    s = proof['s']
    d = proof['d']
    return u_comm, v_comm, s, d

def serialize_proof(proof):
    u_comm, v_comm, s, d = extract_proof(proof)
    return {
        'u_comm': serialize_ecc_point(u_comm),
        'v_comm': serialize_ecc_point(v_comm),
        's': serialize_factor(s),
        'd': serialize_ecc_point(d)
    }

def deserialize_proof(curve, proof):
    u_comm, v_comm, s, d = extract_proof(proof)
    return {
        'u_comm': deserialize_ecc_point(curve, u_comm),
        'v_comm': deserialize_ecc_point(curve, v_comm),
        's': deserialize_factor(s),
        'd': deserialize_ecc_point(curve, d),
    }

def set_ddh_proof(ddh, proof):
    return {
        'ddh': ddh,
        'proof': proof
    }

def extract_ddh_proof(ddh_proof):
    ddh = ddh_proof['ddh']
    proof = ddh_proof['proof']
    return ddh, proof

def serialize_ddh_proof(ddh_proof):
    ddh, proof = extract_ddh_proof(ddh_proof)
    return {
        'ddh': serialize_ddh(ddh),
        'proof': serialize_proof(proof),
    }

def deserialize_ddh_proof(curve, ddh_proof):
    ddh, proof = extract_ddh_proof(ddh_proof)
    return {
        'ddh': deserialize_ddh(curve, ddh),
        'proof': deserialize_proof(curve, proof),
    }

def chaum_pedersen(curve, ddh, z, *extras):
    g = curve.G
    r = random_factor(curve);

    u, v, w = ddh

    u_comm = r * u                                      # u commitment
    v_comm = r * g                                      # g commitment

    c = fiat_shamir(u, v, w, u_comm, v_comm, *extras)   # challenge

    s = (r + c * z) % curve.order                       # response
    d = z * u

    proof = set_proof(u_comm, v_comm, s, d)
    return proof

def chaum_pedersen_verify(curve, ddh, proof, *extras):
    g = curve.G
    u, v, w = ddh
    u_comm, v_comm, s, d = extract_proof(proof)
    c = fiat_shamir(u, v, w, u_comm, v_comm,  *extras)   # challenge
    return (s * u == u_comm + c * d) and \
           (s * g == v_comm + c * v)
 
