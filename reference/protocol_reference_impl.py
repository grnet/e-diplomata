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


# class KeyGenerator(object):
#
#     def __init__(self, curve):
#         self.curve = curve
#
#     def generate(self):
#         key = {
#             'ecc': ECC.generate(curve=self.curve.desc),
#             'nacl': PrivateKey.generate(),
#         }
#         return key

def keygen(curve):
    return {
        'ecc': ECC.generate(curve=curve.desc),
        'nacl': PrivateKey.generate(),
    }


# class Signer(object):
#     pass
#
# class Holder(object):
#     pass
#
# class Issuer(object):
#     pass
#
# class Verifier(object):
#     pass


def ecc_point_to_bytes(ecc_point):
    return ecc_point.x.to_bytes(), ecc_point.y.to_bytes()

def ecc_point_to_str(ecc_point):
    return ecc_point.x.to_bytes(), ecc_point.y.to_bytes()

def gen_curve(curve_name):
    curve = ECC._curves[curve_name]
    return curve

def ecc_pub_key(ecc_key):
    return ecc_key.pointQ

def sign(key, payload):
    signer = DSS.new(key, 'fips-186-3')
    hc = SHA384.new(payload)
    signature = signer.sign(hc)
    return signature

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
    """
    ElGamal encryption
    """
    g = curve.G
    r = random_factor(curve)
    cipher = set_cipher(
        r * g,
        m * g + r * public,
    )
    return cipher, r

def decrypt(key, cipher, table):
    """
    ElGamal decryption
    """
    a, b = extract_cipher(cipher)
    v = b + (key.d * (-a))
    return table[(str(v.x), str(v.y))]

def reencrypt(curve, public, cipher):
    """
    ElGamal re-encryption
    """
    g = curve.G
    r = random_factor(curve)
    c1, c2 = extract_cipher(cipher)
    cipher = set_cipher(
        r * g + c1,
        c2 + r * public,
    )
    return cipher, r

def drenc(cipher, decryptor):
    """
    ElGamal decryption with decryptor
    """
    _, c2 = extract_cipher(cipher)
    m = c2 + (-decryptor)
    return m


# This is taken from https://github.com/kantuni/ZKP
def chaum_pedersen(curve, key, a, b):
    pub = ecc_pub_key(key)
    priv = int(key.d)
    r = random_factor(curve);
    u = a * r
    v = curve.G * r
    to_hash = f'{pub.xy} {a.xy} {b.xy} {u.xy} {v.xy}'.encode('utf-8')
    h = int.from_bytes(SHA384.new(to_hash).digest(), 'big')
    s = (r + h * priv) % curve.order
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

def deserialize_chaum_pedersen(curve, proof):
    a = EccPoint(*proof['a'], curve=curve.desc)
    b = EccPoint(*proof['b'], curve=curve.desc)
    u = EccPoint(*proof['u'], curve=curve.desc)
    v = EccPoint(*proof['v'], curve=curve.desc)
    s = Integer(proof['s'])
    d = EccPoint(*proof['d'], curve=curve.desc)
    return a, b, u, v, s, d


def chaum_pedersen_verify(curve, pub, a, b, u, v, s, d):
    to_hash = f'{pub.xy} {a.xy} {b.xy} {u.xy} {v.xy}'.encode('utf-8')
    h = int.from_bytes(SHA384.new(to_hash).digest(), 'big')
    g = curve.G
    return (a * s == u + d * h) and (g * s == v + pub * h)

def make_table(g, n):
    table = {}
    for i in range(n):
        elem = (i * g)
        table[(str(elem.x), str(elem.y))] = i
    return table

def test_encdec(curve):
    table = make_table(curve.G, 1000)
    # ecc_key = KeyGenerator(curve).generate()['ecc']
    ecc_key = keygen(curve)['ecc']
    pub = ecc_pub_key(ecc_key)
    priv = ecc_pub_key(ecc_key)
    import random
    ps = random.sample(range(1000), 100)
    for i in range(100):
        cipher, r = encrypt(curve, pub, ps[i])
        cipher_r, r_r = reencrypt(curve, pub, cipher)
        assert(decrypt(ecc_key, cipher, table) == ps[i])
        assert(decrypt(ecc_key, cipher_r, table) == ps[i])

def step_one(curve, issuer_key, t):
    # order = curve.order       # Maybe use in payload?
    h = hash_into_integer(t)
    cipher, r = encrypt(curve, ecc_pub_key(issuer_key), h)
    c1, c2 = extract_cipher(cipher)
    payload = f'AWARD c1={c1.xy} c2={c2.xy}'.encode('utf-8')
    s_awd = sign(issuer_key, payload)
    commitment = (c1, c2)
    return s_awd, commitment, r

def step_two(curve, holder_key, verifier_key, s_awd):
    payload = (f'REQUEST s_awd={s_awd} '
               'ver_pub={ecc_pub_key(verifier_key).xy}').encode('utf-8')
    s_req = sign(holder_key, payload)
    return s_req

def step_three(curve, issuer_key, pub_verifier_key, r, commitment, s_req, issuer_box):
    c1, c2 = c
    pub = ecc_pub_key(issuer_key)
    # re-encrypt c
    cipher = set_cipher(c1, c2)
    cipher_r, r_r = reencrypt(curve, pub, cipher)
    c1_r, c2_r = extract_cipher(cipher_r)
    c_r = (c1_r, c2_r)
    # create NIRENC
    proof_c1 = c1, c1_r, *chaum_pedersen(curve, issuer_key, c1, c1_r)
    proof_c2 = c2, c2_r, *chaum_pedersen(curve, issuer_key, c2, c2_r)
    nirenc = (proof_c1, proof_c2)
    nirenc_str = (serialize_chaum_pedersen(*proof_c1),
                  serialize_chaum_pedersen(*proof_c2))
    # create and encrypt decryptor
    g = curve.G
    r_tilde = r + r_r
    decryptor = pub * r_tilde
    enc_decryptor = issuer_box.encrypt(str(decryptor.xy).encode('utf-8'))
    # create and encrypt NIDDH of decryptor
    g_r = g * r
    g_r_r = g * r_r
    u, v, s, d = chaum_pedersen(curve, issuer_key, g_r, g_r_r)
    niddh = serialize_chaum_pedersen(g_r, g_r_r, u, v, s, d)
    enc_niddh = issuer_box.encrypt(json.dumps(niddh).encode('utf-8'))
    payload = (f'PROOF s_req={s_req} c_r=({c_r[0].xy, c_r[1].xy}) '
               f'{nirenc_str} {enc_decryptor} '
               f'{enc_niddh}'.encode('utf-8'))
    s_prf = sign(issuer_key, payload)
    return (s_prf, c_r, nirenc, enc_decryptor, enc_niddh)

def step_four(curve, issuer_key, verifier_key, c_r, nirenc,
              enc_decryptor, enc_niddh, verifier_box, m):
    # get the decryptor
    dec_decryptor = verifier_box.decrypt(enc_decryptor).decode('utf-8')
    extract_coords = re.match(r'^\D*(\d+)\D+(\d+)\D*$', dec_decryptor)
    x_affine = int(extract_coords.group(1))
    y_affine = int(extract_coords.group(2))
    if not extract_coords:
        payload = f'FAIL {s_prf}'.encode('utf-8')
        s_ack = sign(verifier_key, payload)
        return s_ack
    decryptor = ECC.EccPoint(x_affine, y_affine, curve=curve.desc)
    # decrypt the re-encryption using the decryptor
    c1, c2 = c_r
    cipher_r = set_cipher(c1, c2)
    dec_m = drenc(cipher_r, decryptor)
    # check that the decrypted hash is the same with the hash of the original
    # document, as an ECC point
    h = hash_into_integer(m)
    g = curve.G
    h_ecc_point = g * h
    if dec_m != h_ecc_point:
        payload = f'NACK {s_prf}'.encode('utf-8')
        s_ack = sign(verifier_key, payload)
        return s_ack
    # check the NIRENC proof
    proof_c1, proof_c2 = nirenc
    a, b, u, v, s, d = proof_c1
    pub = ecc_pub_key(issuer_key)
    check_proof_c1 = chaum_pedersen_verify(curve, pub, a, b, u, v, s, d)
    if not check_proof_c1:
        payload = f'FAIL {s_prf}'.encode('utf-8')
        s_ack = sign(verifier_key, payload)
        return s_ack
    a, b, u, v, s, d = proof_c2
    check_proof_c2 = chaum_pedersen_verify(curve, pub, a, b, u, v, s, d)
    if not check_proof_c2:
        payload = f'FAIL {s_prf}'.encode('utf-8')
        s_ack = sign(verifier_key, payload)
        return s_ack
    # check the NIDDH proof
    dec_niddh = verifier_box.decrypt(enc_niddh)
    a, b, u, v, s, d = deserialize_chaum_pedersen(curve, json.loads(dec_niddh))
    check_proof_r_r = chaum_pedersen_verify(curve, pub, a, b, u, v, s, d)
    assert(check_proof_r_r)
    if not check_proof_r_r:
        payload = f'FAIL {s_prf}'.encode('utf-8')
        s_ack = sign(verifier_key, payload)
        return s_ack
    payload = f'ACK {s_prf}'.encode('utf-8')
    s_ack = sign(verifier_key, payload)
    return s_ack

if __name__ == '__main__':
    curve = gen_curve('P-384')
    test_encdec(curve)

    # Setup keys

    aux = keygen(curve)
    issuer_key = aux['ecc']
    issuer_nacl_key = aux['nacl']

    aux = keygen(curve)
    holder_key = aux['ecc']
    _ = aux['nacl']

    aux = keygen(curve)
    verifier_key = aux['ecc']
    verifier_nacl_key = aux['nacl']

    #

    m = "This is a message to be encrypted".encode('utf-8')

    issuer_box = Box(issuer_nacl_key, verifier_nacl_key.public_key)
    verifier_box = Box(verifier_nacl_key, issuer_nacl_key.public_key)

    print('step 1')
    s_awd, c, r = step_one(curve, issuer_key, m)
    c1, c2 = c
    print('c1:', c1.xy, 'c2:', c2.xy, 's_awd:', s_awd, 'r:', r)
    print()

    print('step_two')
    s_req  = step_two(curve, holder_key, verifier_key, s_awd)
    print('s_req:', s_req)
    print('step_three')
    s_prf, c_r, nirenc, enc_decryptor, enc_niddh = step_three(
        curve, issuer_key, verifier_key,
        r, (c1, c2), s_req,
        issuer_box)
    print('s_prf:', s_prf)
    print('step_four')
    s_ack = step_four(curve, issuer_key, verifier_key, c_r, nirenc,
                      enc_decryptor, enc_niddh, verifier_box, m)
    print('s_ack:', s_ack)
