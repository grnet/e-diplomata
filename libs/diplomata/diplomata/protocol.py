"""
Transaction Layer
"""

import json
from nacl.public import PrivateKey as _NaclKey
from nacl.public import Box as _NaclBox
from Cryptodome.PublicKey import ECC as _ECC
from diplomata.elgamal import ElGamalCrypto, \
    hash_into_scalar, _ecc_pub, gen_curve
from diplomata.primitives import Prover as _Prover, \
        Verifier as _Verifier, Signer as _Signer
from diplomata.adaptors import _ElGamalSerializer, _KeySerializer
from diplomata.util import *

AWARD   = 'AWARD'
REQUEST = 'REQUEST'
PROOF   = 'PROOF'
ACK     = 'ACK'
NACK    = 'NACK'
FAIL    = 'FAIL'


def _nacl_pub(nacl_key):
    return nacl_key.public_key

def _extract_public_keys(key):
    ecc_key, nacl_key = extract_keys(key)
    ecc_pub  = _ecc_pub(ecc_key)
    nacl_pub = _nacl_pub(nacl_key)
    return ecc_pub, nacl_pub


class KeyManager(_KeySerializer):

    def __init__(self, curve='P-384', hexifier=True, flattener=False):
        self._cryptosys = ElGamalCrypto(curve)
        super().__init__(curve, hexifier=hexifier, flattener=flattener)

    def _generate_elgamal_key(self):
        return self._cryptosys.generate_key()

    def _generate_nacl_key(self):
        return _NaclKey.generate()

    def generate_keys(self, serialized=True):
        ecc_key  = self._generate_elgamal_key()
        nacl_key = self._generate_nacl_key()
        keys = set_keys(ecc_key, nacl_key)
        if serialized is True:
            keys = self._serialize_key(keys)
        return keys

    def get_public_shares(self, key, serialized=True, from_serialized=True):
        if from_serialized:
            key = self._deserialize_key(key)
        ecc_pub, nacl_pub = _extract_public_keys(key)
        if serialized:
            ecc_pub  = self.serialize_ecc_public(ecc_pub)
            nacl_pub = self._serialize_nacl_public(nacl_pub)
        public_shares = set_keys(ecc_pub, nacl_pub)
        public = self._flatten_public(public_shares)
        return public


class Party(_ElGamalSerializer):
    """
    Common infrastructure for Holder, Issuer and Verifier
    """

    def __init__(self, curve='P-384', key=None, hexifier=True, flattener=False):
        self._cryptosys = ElGamalCrypto(curve)
        self._key_manager = KeyManager(curve, hexifier=hexifier,
                flattener=flattener)
        if key is None:
            self._key = self._key_manager.generate_keys(serialized=False)
        else:
            self._key = self._key_manager._deserialize_key(key)
        super().__init__(curve, hexifier=hexifier, flattener=flattener)
        self._signer = _Signer(curve)

    @classmethod
    def from_key(cls, key, curve='P-384', hexifier=True, flattener=False):
        return cls(key=key, curve=curve, hexifier=hexifier, flattener=flattener)

    def get_public(self, serialized=True):
        return self._key_manager.get_public_shares(self._key,
            serialized=serialized, from_serialized=False)       # TODO

    @property
    def _keys(self):
        ecc_key, nacl_key = extract_keys(self._key)
        return ecc_key, nacl_key

    @property
    def public_keys(self):
        ecc_pub, nacl_pub = _extract_public_keys(self._key)
        return ecc_pub, nacl_pub

    @property
    def _elgamal_key(self):
        ecc_key, _ = self._keys
        return ecc_key

    @property
    def elgamal_pub(self):
        ecc_pub, _ = self.public_keys
        return ecc_pub

    @property
    def _nacl_key(self):
        _, nacl_key = self._keys
        return nacl_key

    @property
    def nacl_pub(self):
        _, nacl_pub = self.public_keys
        return nacl_pub

    def deserialize_public(self, public):
        return self._key_manager.deserialize_public(public)

    def encode(self, entity, serializer):
        return json.dumps(serializer(
            entity)).encode('utf-8')

    def decode(self, entity, deserializer):
        return deserializer(json.loads(
            entity.decode('utf-8')))

    def nacl_encrypt(self, content, receiver_pub):
        box = _NaclBox(self._nacl_key, receiver_pub['nacl'])
        cipher = box.encrypt(content).hex()
        return cipher

    def nacl_decrypt(self, cipher, sender_pub):
        box = _NaclBox(self._nacl_key, sender_pub['nacl'])
        plaintxt = box.decrypt(bytes.fromhex(cipher))
        return plaintxt

    def elgamal_encrypt(self, pub, m):
        cipher, r = self._cryptosys.encrypt(pub, m)
        return cipher, r

    def elgamal_decrypt(self, cipher, decryptor):
        elem = self._cryptosys.decrypt_with_decryptor(cipher, decryptor)
        return elem

    def serialize_document(self, title):
        return title.decode('utf-8')

    def deserialize_document(self, title):
        return title.encode('utf-8')

    def hash_document(self, title):
        title = self.deserialize_document(title) if \
            isinstance(title, str) else title
        out = self._cryptosys.hash_into_element(title)  # H(t) * g
        return out

    @staticmethod
    def create_tag(label, *args, **kwargs):
        out = label
        for arg in args:
            out += f' {arg}'
        for (key, value) in kwargs.items():
            out += f' {key}={value}'
        return out.encode('utf-8')

    def sign(self, message, serialized=True):
        signature = self._signer.sign(self._elgamal_key, message)
        if serialized is True:
            signature = self.serialize_signature(signature)
        return signature

    def verify_signature(self, sig, pub, message, from_serialized=True):
        pub = pub['ecc']
        if from_serialized is True:
            sig = self.deserialize_signature(sig)
            pub = self._key_manager.deserialize_ecc_public(pub)
        verified = self._signer.verify_signature(
            sig, pub, message)
        return verified


class Holder(Party):

    def __init__(self, curve='P-384', key=None, hexifier=True, flattener=False):
        super().__init__(curve, key, hexifier=hexifier, flattener=flattener)

    def publish_request(self, s_awd, ver_pub):
        payload = self.create_tag(REQUEST, s_awd=s_awd, verifier=ver_pub)
        s_req = self.sign(payload)
        return s_req


class Issuer(Party):

    def __init__(self, curve='P-384', key=None, hexifier=True, flattener=False):
        super().__init__(curve, key, hexifier=hexifier, flattener=flattener)
        self._prover = _Prover(curve)

    def commit_to_document(self, title):
        ht = self.hash_document(title)          # H(t) * g
        pub = self.elgamal_pub                  # I
        c, r = self.elgamal_encrypt(pub, ht)    # r * g, H(t) * g + r * I
        return c, r

    def publish_award(self, title):
        title = self.deserialize_document(title)

        c, r = self.commit_to_document(title)       # r * g, H(t) * g + r * I

        c = self.serialize_cipher(c)
        r = self.serialize_scalar(r)

        payload = self.create_tag(AWARD, c=c)
        s_awd = self.sign(payload)
        return s_awd, c, r

    def elgamal_reencrypt(self, pub, c):
        c_r, r_r = self._cryptosys.reencrypt(pub, c)
        return c_r, r_r

    def reencrypt_commitment(self, c):
        pub = self.elgamal_pub                      # I
        c_r, r_r = self.elgamal_reencrypt(pub, c)   # (r1 + r2) * g, H(t) * g + (r1 + r2) * I
        return c_r, r_r

    def prove_renc(self, c, c_r, r_r):
        pub = self.elgamal_pub
        nirenc = self._prover.prove_reencryption(c, c_r, r_r, pub)
        return nirenc

    def create_decryptor(self, r):
        pub = self.elgamal_pub                                  # I
        decryptor = self._cryptosys.create_decryptor(r, pub)    # r * I
        return decryptor

    def prove_dec(self, c_r, decryptor, r, r_r):
        pub = self.elgamal_pub
        nidec = self._prover.prove_decryption(c_r, decryptor, r + r_r, pub)
        return nidec

    def generate_proof(self, c, r):
        c_r, r_r = self.reencrypt_commitment(c)             # (r + r') * g, H(t) * g + (r + r') * I
        decryptor = self.create_decryptor(r + r_r)          # (r + r') * I
        nirenc = self.prove_renc(c, c_r, r_r)               # NIRENC_I(c, c')
        nidec = self.prove_dec(c_r, decryptor, r, r_r)      # NIDDH_I(r + r')
        proof = set_proof(c_r, decryptor, nirenc, nidec)
        return proof

    def nacl_encrypt_decryptor(self, decryptor, pub):
        decryptor = self.encode(decryptor, 
            serializer=self.serialize_ecc_point)
        enc_decryptor = self.nacl_encrypt(decryptor, pub)   # E_V((r1 + r2) * I)
        return enc_decryptor

    def nacl_encrypt_nidec(self, nidec, pub):
        nidec = self.encode(nidec, 
            serializer=self.serialize_nidec)
        enc_nidec = self.nacl_encrypt(nidec, pub)
        return enc_nidec

    def nacl_encrypt_proof(self, proof, ver_pub):
        """
        Symmetrically encrypt decryptor and proof of decryption
        """
        c_r, decryptor, nirenc, nidec = extract_proof(proof)
        enc_decryptor = self.nacl_encrypt_decryptor(
            decryptor, ver_pub)                                     # E_V((r + r') * I)
        enc_nidec = self.nacl_encrypt_nidec(nidec, ver_pub)         # E_V(NIDDH_I(r + r'))
        proof = set_proof(c_r, enc_decryptor, nirenc, enc_nidec)
        return proof

    def publish_proof(self, s_req, r, c, ver_pub):
        r = self.deserialize_scalar(r)
        c = self.deserialize_cipher(c)
        ver_pub = self.deserialize_public(ver_pub)

        proof = self.generate_proof(c, r)

        proof = self.nacl_encrypt_proof(proof, ver_pub)
        proof = self.serialize_proof(proof)
        payload = self.create_tag(PROOF, s_req=s_req, **proof)
        s_prf = self.sign(payload)

        return s_prf, proof


class Verifier(Party):

    def __init__(self, curve='P-384', key=None, hexifier=True, flattener=False):
        super().__init__(curve, key, hexifier=hexifier, flattener=flattener)
        self._verifier = _Verifier(curve)

    def nacl_decrypt_decryptor(self, issuer_pub, enc_decryptor):
        decryptor = self.nacl_decrypt(enc_decryptor, issuer_pub)
        return self.decode(decryptor, self.deserialize_ecc_point)

    def nacl_decrypt_nidec(self, issuer_pub, enc_nidec):
        nidec = self.nacl_decrypt(enc_nidec, issuer_pub)
        return self.decode(nidec, self.deserialize_nidec)

    def nacl_decrypt_proof(self, proof, issuer_pub):
        """
        Symmetrically decrypt decryptor and proof of decryption
        """
        c_r, enc_decryptor, nirenc, enc_nidec = extract_proof(proof)
        decryptor = self.nacl_decrypt_decryptor(
            issuer_pub, enc_decryptor)                              # (r + r') * I
        nidec = self.nacl_decrypt_nidec(issuer_pub, enc_nidec)      # NIDDH_I(r + r')
        proof = set_proof(c_r, decryptor, nirenc, nidec)
        return proof

    def decrypt_commitment(self, c_r, decryptor):
        c_dec = self.elgamal_decrypt(c_r, decryptor)
        return c_dec

    def verify_document_integrity(self, t, c_dec):
        return c_dec == self.hash_document(t)                       # c_dec == H(t) * g?

    def verify_nirenc(self, nirenc, issuer_pub):
        pub = issuer_pub['ecc']
        return self._verifier.verify_ddh_proof(nirenc, pub)

    def verify_nidec(self, nidec, issuer_pub):
        pub = issuer_pub['ecc']
        return self._verifier.verify_ddh_proof(nidec, pub)

    def verify_proof(self, proof, title, issuer_pub):
        c_r, decryptor, nirenc, nidec = extract_proof(proof)

        # Decrypt the issuer's initial commitment to document
        c_dec = self.decrypt_commitment(c_r, decryptor)

        # Verifications
        check_title     = self.verify_document_integrity(title, c_dec)
        check_nirenc    = self.verify_nirenc(nirenc, issuer_pub)
        check_nidec     = self.verify_nidec(nidec, issuer_pub)

        # Verification result
        result = all((
            check_title, 
            check_nirenc, 
            check_nidec,
        ))
        return result

    def publish_ack(self, s_prf, title, proof, issuer_pub):
        title = self.deserialize_document(title)
        proof = self.deserialize_proof(proof)
        issuer_pub = self.deserialize_public(issuer_pub)

        proof = self.nacl_decrypt_proof(proof, issuer_pub)
        result = self.verify_proof(proof, title, issuer_pub)

        payload = self.create_tag(
            ACK if result else NACK,
            result=result,
            s_prf=s_prf)
        s_ack = self.sign(payload)

        return s_ack, result
