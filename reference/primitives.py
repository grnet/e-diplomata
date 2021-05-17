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

    def encrypt(self, public, m):
        cipher, r = self.cryptosys.encrypt(public, m)
        return cipher, r

    def reencrypt(self, public, cipher):    
        cipher, r = self.cryptosys.reencrypt(public, cipher)
        return cipher, r

    # TODO: Make clear the meaning of this function with respet to ElGamal
    # encryption and rename appropriately
    def commit(self, public, t):
        ht = hash_into_integer(t)           # H(t)
        c, r = self.encrypt(public, ht)     # (r * g, H(t) * g + r * I), r
        return c, r

    def reencrypt_commitment(self, c):
        pub = self.public
        c_r, r_r = self.elgamal_reencrypt(pub, c)
        return c_r, r_r

    def create_decryptor(self, r1, r2, verifier_pub):
        r_tilde = r1 + r2
        pub = self.public
        decryptor =  r_tilde * pub              # TODO

        # TODO: Transfer one layer above
        enc_decryptor = self.encrypt(
            str(decryptor.xy).encode('utf-8'),  # TODO
            verifier_pub
        )

        return decryptor, enc_decryptor

    def generate_nirenc(self, c, c_r, verifier_pub):
        c1  , c2   = extract_cipher(c)
        c1_r, c2_r = extract_cipher(c_r)

        priv = self.private                     # TODO
        pub = self.public                       # TODO
        extras = (pub,)

        # TODO:
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

    def generate_niddh(self, r1, r2, verifier_pub):
        g = self.generator

        g_r   = r1 * g
        g_r_r = r2 * g

        # priv, pub = self.elgamal_key
        priv = self.private                     # TODO
        pub = self.public                       # TODO
        extras = (pub,)

        # TODO
        niddh = set_ddh_proof(
            (g_r, pub, g_r_r),
            self._generate_chaum_pedersen((g_r, pub, g_r_r), priv, *extras)
        )
        niddh = self._serialize_ddh_proof(niddh)

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

