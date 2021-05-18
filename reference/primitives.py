import json
import re
from nacl.public import PrivateKey, Box
from Cryptodome.Signature import DSS
from Cryptodome.Hash import SHA384
from elgamal import ElGamalCrypto, Signer
from structs import *
from util import hash_into_integer


class KeyOwner(object):
    """
    ElGamal-key owner interface
    """

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
        return cipher, r                        # (r1 + r2) * g, m * g + (r1 + r2) * y

    def generate_decryptor(self, r1, r2, pub):
        return (r1 + r2) * pub

    def _generate_chaum_pedersen(self, ddh, z, *extras):
        return self.cryptosys.generate_chaum_pedersen(ddh, z, *extras)

    def generate_nirenc(self, c, c_r, keypair=None):
        c1  , c2   = extract_cipher(c)
        c1_r, c2_r = extract_cipher(c_r)

        priv, pub = self.keypair if not keypair \
            else keypair
        extras = (pub,)                         # TODO: Maybe enhance extras

        proof_c1 = set_ddh_proof(
            (c1, pub, c1_r),
            self._generate_chaum_pedersen((c1, pub, c1_r), priv, *extras)
        )
        proof_c2 = set_ddh_proof(
            (c2, pub, c2_r),
            self._generate_chaum_pedersen((c2, pub, c2_r), priv, *extras)
        )

        nirenc = set_nirenc(proof_c1, proof_c2)
        return nirenc

    def generate_niddh(self, r1, r2, keypair=None):
        g = self.generator

        g_r   = r1 * g
        g_r_r = r2 * g

        priv, pub = self.keypair if not keypair \
            else keypair
        extras = (pub,)                         # TODO: Maybe enhance extras

        niddh = set_ddh_proof(
            (g_r, pub, g_r_r),
            self._generate_chaum_pedersen((g_r, pub, g_r_r), priv, *extras)
        )

        return niddh


class Verifier(KeyOwner):

    def __init__(self, curve='P-384', key=None):
        self.cryptosys = ElGamalCrypto(curve)
        super().__init__(self.cryptosys, key=key)

    @property
    def generator(self):
        return self.cryptosys.generator

    def _verify_chaum_pedersen(self, ddh, proof, *extras):
        return self.cryptosys.verify_chaum_pedersen(ddh, proof, *extras)

    def verify_message_integrity(self, m, c):
        g = self.generator
        return c == m * g

    def verify_nirenc(self, nirenc, prover_pub):

        proof_c1, proof_c2 = extract_nirenc(nirenc)
        extras = (prover_pub,)                  # TODO: Maybe enhance extras?

        ddh, proof = extract_ddh_proof(proof_c1)
        check_proof_c1 = self._verify_chaum_pedersen(ddh, proof, *extras)
        assert check_proof_c1                   # TODO: Remove

        ddh, proof = extract_ddh_proof(proof_c2)
        check_proof_c2 = self._verify_chaum_pedersen(ddh, proof, *extras)
        assert check_proof_c2                   # TODO: Remove

        return check_proof_c1 and check_proof_c2

    def verify_niddh(self, niddh, prover_pub):
        ddh, proof = extract_ddh_proof(niddh)
        extras = (prover_pub,)                  # TODO: Maybe enchance extras?
        return self._verify_chaum_pedersen(ddh, proof, *extras)

