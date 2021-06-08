from diplomata.elgamal import ElGamalCrypto
from diplomata.util import *

CURVE = 'P-384'

cryptosys = ElGamalCrypto(curve=CURVE)


def test_encryption():
    g = cryptosys.generator
    x = cryptosys.random_scalar()       # private
    y = x * g                           # public
    m = cryptosys.random_scalar() * g   # message
    c, r = cryptosys.encrypt(y, m)
    assert m == cryptosys.decrypt(x, c)

def test_decryption_with_decryptor():
    g = cryptosys.generator
    x = cryptosys.random_scalar()       # private
    y = x * g                           # public
    m = cryptosys.random_scalar() * g   # message
    c, r = cryptosys.encrypt(y, m)
    d = cryptosys.create_decryptor(r, y)
    assert cryptosys.decrypt_with_decryptor(c, d) == \
        cryptosys.decrypt(x, c)

def test_reencryption():
    g = cryptosys.generator
    p = cryptosys.order
    x = cryptosys.random_scalar()       # private
    y = x * g                           # public
    m = cryptosys.random_scalar() * g   # message

    c  , r   = cryptosys.encrypt(y, m)
    c_r, r_r = cryptosys.reencrypt(y, c)
    
    assert c_r == set_cipher(
        (r + r_r) % p * g,
        (r + r_r) % p * y + m
    )
    assert m == cryptosys.decrypt(x, c_r)
    d = cryptosys.create_decryptor((r + r_r) % p, y)
    assert m == cryptosys.decrypt_with_decryptor(c_r, d)

def test_chaum_pedersen():
    g = cryptosys.generator

    x = cryptosys.random_scalar()
    z = cryptosys.random_scalar()

    # success
    ddh = (x * g, z * g, x * (z * g))
    proof = cryptosys.generate_chaum_pedersen(ddh, z)
    verified = cryptosys.verify_chaum_pedersen(ddh, proof)
    assert verified

    # corrupt witness
    ddh = (x * g, z * g, x * (z * g))
    proof = cryptosys.generate_chaum_pedersen(ddh, z + 1)
    ddh = (x * g, z * g, x * (z * g))
    verified = cryptosys.verify_chaum_pedersen(ddh, proof)
    assert not verified

    # corrupt ddh
    ddh = (x * g, z * g, x * (z * g))
    proof = cryptosys.generate_chaum_pedersen(ddh, z)
    ddh = (x * g, (z + 1) * g, x * (z * g))
    verified = cryptosys.verify_chaum_pedersen(ddh, proof)
    assert not verified

    # corrupt proof/challenge
    ddh = (x * g, z * g, x * (z * g))
    proof = cryptosys.generate_chaum_pedersen(ddh, z)
    proof['challenge'] += 1
    verified = cryptosys.verify_chaum_pedersen(ddh, proof)
    assert not verified

    # corrupt proof/response
    ddh = (x * g, z * g, x * (z * g))
    proof = cryptosys.generate_chaum_pedersen(ddh, z)
    proof['response'] += 1
    verified = cryptosys.verify_chaum_pedersen(ddh, proof)
    assert not verified

