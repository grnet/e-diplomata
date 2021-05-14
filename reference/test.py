from util import *
from protocol import *


def make_table(g, n):
    table = {}
    for i in range(n):
        elem = (i * g)
        table[(str(elem.x), str(elem.y))] = i
    return table 


def test_elgamal_encdec():
    curve = gen_curve('P-384')

    table = make_table(curve.G, 1000)

    party_1 = Party(curve)
    party_2 = Party(curve)

    key_1 = party_1.key['ecc']
    key_2 = party_2.key['ecc']

    pub_1 = ecc_pub_key(key_1)
    pub_2 = ecc_pub_key(key_2)

    import random
    ps = random.sample(range(1000), 100)
    for i in range(100):
        cipher, r = party_1.elgamal_encrypt(pub_2, ps[i])
        cipher_r, r_r = party_1.elgamal_reencrypt(pub_2, cipher)        
        assert(party_2.elgamal_decrypt(cipher, table) == ps[i])
        assert(party_2.elgamal_decrypt(cipher_r, table) == ps[i])
