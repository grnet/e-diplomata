from diplomata.util import *
from diplomata.protocol import *
from diplomata.elgamal import *

CURVE = 'P-384'

def make_table(curve, n):
    g = gen_curve(name=curve).G
    table = {}
    for i in range(n):
        elem = (i * g)
        table[(str(elem.x), str(elem.y))] = i
    return table 


def test_elgamal_encdec():

    table = make_table(CURVE, 1000)     # lookup table

    party_1 = Issuer(CURVE)
    party_2 = Verifier(CURVE)

    pub_1 = party_1.get_public_shares(serialized=False)
    pub_2 = party_2.get_public_shares(serialized=False)

    import random
    ps = random.sample(range(1000), 100)
    for i in range(100):
        verifier_pub  = pub_2['ecc']
        verifier_priv = party_2._verifier.private
        cryptosys = party_1._cryptosys
        cipher, r = cryptosys.encrypt(verifier_pub, ps[i])
        cipher_r, r_r = cryptosys.reencrypt(verifier_pub, cipher)        
        assert(cryptosys.decrypt(verifier_priv, cipher,   table) == ps[i])
        assert(cryptosys.decrypt(verifier_priv, cipher_r, table) == ps[i])
