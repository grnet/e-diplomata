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
