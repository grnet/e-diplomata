from structs import *
from util import *
from protocol import *


def make_table(curve_name, n):
    g = gen_curve(curve_name).G
    table = {}
    for i in range(n):
        elem = (i * g)
        table[(str(elem.x), str(elem.y))] = i
    return table 


def test_elgamal_encdec():
    CURVE = 'P-384'

    table = make_table(CURVE, 1000)     # lookup table

    party_1 = Issuer(CURVE)
    party_2 = Verifier(CURVE)

    pub_1 = party_1.get_public_shares()
    pub_2 = party_2.get_public_shares()

    import random
    ps = random.sample(range(1000), 100)
    for i in range(100):
        cipher, r = party_1.elgamal_encrypt(pub_2, ps[i])
        cipher_r, r_r = party_1.elgamal_reencrypt(pub_2, cipher)        
        assert(party_2.elgamal_decrypt(cipher, table) == ps[i])
        assert(party_2.elgamal_decrypt(cipher_r, table) == ps[i])
