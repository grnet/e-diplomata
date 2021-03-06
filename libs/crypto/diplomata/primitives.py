"""
Basic Crypto Layer
"""

from Cryptodome.PublicKey import ECC
from Cryptodome.Signature import DSS
from Cryptodome.Hash import SHA384
from diplomata.elgamal import ElGamalCrypto
from diplomata.util import *


class Prover(object):

    def __init__(self, curve='P-384'):
        self._cryptosys = ElGamalCrypto(curve)

    def _generate_chaum_pedersen(self, ddh, z, *extras):
        return self._cryptosys.generate_chaum_pedersen(ddh, z, *extras)

    def prove_reencryption(self, c, c_r, r_r, pub):
        c1  , c2   = extract_cipher(c)              # r * g, m + r * y
        c1_r, c2_r = extract_cipher(c_r)            # (r + r') * g, m + (r + r') * y

        extras = (pub,)

        ddh = (
            pub,                    # x * g
            c1_r + (-c1),           # r' * g
            c2_r + (-c2),           # r' * y = r' * x * g
        )
        proof = self._generate_chaum_pedersen(ddh, r_r, *extras)
        nirenc = set_ddh_proof(ddh, proof)
        return nirenc

    def prove_decryption(self, c, decryptor, r, pub):
        c_1, _ = extract_cipher(c)                          # r * g

        extras = (pub,)

        ddh = (
            pub,                    # x * g
            c_1,                    # r * g
            decryptor,              # r * y = r * x * g
        )
        proof = self._generate_chaum_pedersen(ddh, r, *extras)
        nidec = set_ddh_proof(ddh, proof)
        return nidec


class Verifier(object):

    def __init__(self, curve='P-384'):
        self._cryptosys = ElGamalCrypto(curve)

    def _verify_chaum_pedersen(self, ddh, proof, *extras):
        return self._cryptosys.verify_chaum_pedersen(ddh, proof, *extras)

    def verify_ddh_proof(self, ddh_proof, pub):
        ddh, proof = extract_ddh_proof(ddh_proof)
        extras = (pub,)
        verified = self._verify_chaum_pedersen(ddh, proof, *extras)
        return verified


class Signer(object):

    def __init__(self, curve='P-384', spec='fips-186-3'):
        self.curve = curve
        self.spec = spec

    def _adjust_public(self, pub):
        return ECC.construct(
            curve=self.curve,
            point_x=pub.xy[0],
            point_y=pub.xy[1],
        )

    def sign(self, key, message):
        signer = DSS.new(key, self.spec)
        hmsg = SHA384.new(message)
        signature = signer.sign(hmsg)
        return signature

    def verify_signature(self, sig, pub, message):
        pub = self._adjust_public(pub)
        verifier = DSS.new(pub, self.spec)
        hmsg = SHA384.new(message)
        try:
            verifier.verify(hmsg, sig)
        except ValueError:
            return False
        return True
