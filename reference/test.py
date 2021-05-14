from util import *
from protocol import *

def test_elgamal_encdec():
    curve = gen_curve('P-384')
    table = make_table(curve.G, 1000)
    ecc_key = Party(curve)._keygen(curve)['ecc']
    pub = ecc_pub_key(ecc_key)
    priv = ecc_pub_key(ecc_key)
    import random
    ps = random.sample(range(1000), 100)
    for i in range(100):
        cipher, r = elgamal_encrypt(curve, pub, ps[i])
        cipher_r, r_r = elgamal_reencrypt(curve, pub, cipher)        
        assert(elgamal_decrypt(ecc_key, cipher, table) == ps[i])
        assert(elgamal_decrypt(ecc_key, cipher_r, table) == ps[i])
