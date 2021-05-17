from Cryptodome.PublicKey import ECC
from Cryptodome.Hash import SHA384

from Cryptodome.PublicKey.ECC import EccPoint
from Cryptodome.Math.Numbers import Integer

import nacl.utils


def gen_curve(curve_name):
    curve = ECC._curves[curve_name]
    return curve


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
