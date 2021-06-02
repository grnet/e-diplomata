"""
Basic Crypto Layer
"""

from diplomata.elgamal import ElGamalCrypto
from diplomata.util import *


class KeyOwner(object):

    def __init__(self, cryptosys, key=None):
        self.key = key

    @property
    def private(self):
        return self.key.d

    @property
    def public(self):
        return self.key.pointQ

    @property
    def keypair(self):
        return self.private, self.public


class Prover(KeyOwner):

    def __init__(self, curve='P-384', key=None):
        self.cryptosys = ElGamalCrypto(curve)
        super().__init__(self.cryptosys, key=key)

    @property
    def generator(self):
        return self.cryptosys.generator

    def commit(self, elem, pub=None):
        pub = self.public if not pub else pub       # y
        c, r = self.cryptosys.encrypt(pub, elem)    # r * g, m * g + r * y
        return c, r

    def reencrypt(self, pub, cipher):
        cipher, r = self.cryptosys.reencrypt(
            pub, cipher)
        return cipher, r                            # (r1 + r2) * g, m * g + (r1 + r2) * y

    def generate_decryptor(self, r1, r2, pub):
        return (r1 + r2) * pub

    def _generate_chaum_pedersen(self, ddh, z, *extras):
        return self.cryptosys.generate_chaum_pedersen(ddh, z, *extras)

    def generate_nirenc(self, c, c_r, r_r, keypair=None):
        c1  , c2   = extract_cipher(c)                      # r * g, m + r * y
        c1_r, c2_r = extract_cipher(c_r)                    # s * g, m + s * y

        _, y = self.keypair if not keypair \
            else keypair
        extras = (y,)

        ddh = (
            y,                      # x * g 
            c1_r + (-c1),           # r' * g
            c2_r + (-c2),           # r' * y = r' * x * g
        )
        nirenc = set_ddh_proof(
            ddh,
            self._generate_chaum_pedersen(ddh, r_r, *extras)
        )
        return nirenc

    def generate_niddh(self, c_r, decryptor, s, keypair=None):
        c_r_1, _ = extract_cipher(c_r)                      # s * g

        _, y = self.keypair if not keypair \
            else keypair
        extras = (y,)

        ddh = (
            y,                      # x * g
            c_r_1,                  # s * g
            decryptor,              # s * y = s * x * g
        )
        niddh = set_ddh_proof(
            ddh,
            self._generate_chaum_pedersen(ddh, s, *extras)
        )
        return niddh


class Verifier(KeyOwner):

    def __init__(self, curve='P-384', key=None):
        self.cryptosys = ElGamalCrypto(curve)
        super().__init__(self.cryptosys, key=key)

    def _verify_chaum_pedersen(self, ddh, proof, *extras):
        return self.cryptosys.verify_chaum_pedersen(ddh, proof, *extras)

    def verify_nirenc(self, nirenc, prover_pub):
        ddh, proof = extract_nirenc(nirenc)
        extras = (prover_pub,)                  # TODO: Maybe enhance extras?
        verified = self._verify_chaum_pedersen(ddh, proof, *extras)
        return verified

    def verify_niddh(self, niddh, prover_pub):
        ddh, proof = extract_ddh_proof(niddh)
        extras = (prover_pub,)                  # TODO: Maybe enchance extras?
        verified = self._verify_chaum_pedersen(ddh, proof, *extras)
        return verified
