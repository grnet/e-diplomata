from diplomata.elgamal import ElGamalCrypto

CURVE = 'P-384'

cryptosys = ElGamalCrypto(curve=CURVE)


def test_encryption():
    g = cryptosys.generator
    x = cryptosys.random_scalar()       # private key
    y = x * g                           # public key
    m = cryptosys.random_scalar() * g   # message
    c, _ = cryptosys.encrypt(y, m)
    assert m == cryptosys.decrypt(x, c)
