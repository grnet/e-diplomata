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

