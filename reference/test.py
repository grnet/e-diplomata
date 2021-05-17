from structs import *
from util import *
from protocol import *

CURVE = 'P-384'

def make_table(curve_name, n):
    g = gen_curve(curve_name).G
    table = {}
    for i in range(n):
        elem = (i * g)
        table[(str(elem.x), str(elem.y))] = i
    return table 


def test_elgamal_encdec():

    table = make_table(CURVE, 1000)     # lookup table

    party_1 = Issuer(CURVE)
    party_2 = Verifier(CURVE)

    pub_1 = party_1.get_public_shares()
    pub_2 = party_2.get_public_shares()

    import random
    ps = random.sample(range(1000), 100)
    for i in range(100):
        cipher, r = party_1.prover.encrypt(pub_2['ecc'], ps[i])
        cipher_r, r_r = party_1.prover.reencrypt(pub_2['ecc'], cipher)        
        assert(party_2.verifier.decrypt(cipher, table) == ps[i])
        assert(party_2.verifier.decrypt(cipher_r, table) == ps[i])
