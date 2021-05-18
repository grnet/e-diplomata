import json
import re
from nacl.public import PrivateKey, Box
from Cryptodome.Signature import DSS
from Cryptodome.Hash import SHA384
from crypto import ElGamalCrypto, Signer, KeyOwner, ElGamalWrapper
from structs import *
from util import hash_into_integer


class Prover(ElGamalWrapper, KeyOwner):

    def __init__(self, curve='P-384', key=None):
        self.cryptosys = ElGamalCrypto(curve)
        super().__init__(self.cryptosys, key=key)

    def encrypt(self, pub, elem):
        cipher, r = self.cryptosys.encrypt(pub, elem)
        return cipher, r

    def commit(self, elem, pub=None):
        pub = self.public if not pub else pub   # y
        c, r = self.encrypt(pub, elem)          # r * g, m * g + r * y
        return c, r

    def reencrypt(self, pub, cipher):    
        cipher, r = self.cryptosys.reencrypt(
            pub, cipher)
        return cipher, r                        # (r1 + r2) * g, m * g + (r1 + r2) * y

    def generate_decryptor(self, r1, r2, pub):
        return (r1 + r2) * pub

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


class Verifier(ElGamalWrapper, KeyOwner):

    def __init__(self, curve='P-384', key=None):
        self.cryptosys = ElGamalCrypto(curve)
        super().__init__(self.cryptosys, key=key)

    def decrypt(self, cipher, table):
        priv = self.private
        return self.cryptosys.decrypt(priv, cipher, table)
 
    def drenc(self, cipher, decryptor):
        return self.cryptosys.drenc(cipher, decryptor)

    def decrypt_commitment(self, c_r, decryptor):
        dec_m = self.drenc(c_r, decryptor)
        return dec_m

    def check_message_integrity(self, message, dec_m):
        """
        Checks that dec_m coincides with the hash of message,
        seen as ECC points
        """
        g = self.generator
        h = hash_into_integer(message)
        h_ecc_point = h * g
        return dec_m == h_ecc_point

    def verify_nirenc(self, nirenc, issuer_pub):

        proof_c1, proof_c2 = extract_nirenc(nirenc)
        extras = (issuer_pub['ecc'],)

        ddh, proof = extract_ddh_proof(proof_c1)
        check_proof_c1 = self._verify_chaum_pedersen(ddh, proof, *extras)
        assert check_proof_c1   # TODO: Remove

        ddh, proof = extract_ddh_proof(proof_c2)
        check_proof_c2 = self._verify_chaum_pedersen(ddh, proof, *extras)
        assert check_proof_c2   # TODO: Remove

        return check_proof_c1 and check_proof_c2

    def verify_niddh(self, niddh, issuer_pub):
        ddh, proof = extract_ddh_proof(niddh)
        extras = (issuer_pub['ecc'],)                           # TODO
        return self._verify_chaum_pedersen(ddh, proof, *extras)

