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

    def get_public_from_key(self, key, serialized=True, from_serialized=True):
        if from_serialized:
            key = self._deserialize_key(key)
        ecc_pub, nacl_pub = _extract_public_keys(key)
        if serialized:
            ecc_pub  = self.serialize_ecc_public(ecc_pub)
            nacl_pub = self._serialize_nacl_public(nacl_pub)
        public_shares = set_keys(ecc_pub, nacl_pub)
        public_shares = self._flatten_public(public_shares)
        return public_shares


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
        return self._key_manager.get_public_from_key(self._key,
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

    def encode(self, entity, serializer):
        return json.dumps(serializer(
            entity)).encode('utf-8')

    def decode(self, entity, deserializer):
        return deserializer(json.loads(
            entity.decode('utf-8')))

    def encrypt(self, content, receiver_pub):
        """
        Symmetric encryption (nacl common secret)
        """
        box = _NaclBox(self._nacl_key, receiver_pub['nacl'])
        cipher = box.encrypt(content).hex()
        return cipher

    def decrypt(self, cipher, sender_pub):
        """
        Symmetric decryption (nacl common secret)
        """
        box = _NaclBox(self._nacl_key, sender_pub['nacl'])
        content = box.decrypt(bytes.fromhex(cipher))
        return content

    def hash_document(self, title):
        payload = title.encode('utf-8') if \
            isinstance(title, str) else title
        out = self._cryptosys.hash_into_element(payload)  # H(t) * g
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

    def verify_signature(self, sig, signer_pub, message, from_serialized=True):
        pub = signer_pub['ecc']    # TODO
        if from_serialized is True:
            sig = self.deserialize_signature(sig)
            pub = self._key_manager.deserialize_ecc_public(pub)
        verified = self._signer.verify_signature(
            sig, pub, message)
        return verified


class Holder(Party):

    def __init__(self, curve='P-384', key=None, hexifier=True, flattener=False):
        super().__init__(curve, key, hexifier=hexifier, flattener=flattener)

    def publish_request(self, s_awd, verifier_pub):
        payload = self.create_tag(REQUEST, s_awd=s_awd, verifier=verifier_pub)
        s_req = self.sign(payload)
        return s_req


class Issuer(Party):

    def __init__(self, curve='P-384', key=None, hexifier=True, flattener=False):
        super().__init__(curve, key, hexifier=hexifier, flattener=flattener)
        self._prover = _Prover(curve)

    def commit_to_document(self, title):
        ht = self.hash_document(title)                  # H(t) * g
        pub = self.elgamal_pub                          # I
        c, r = self._cryptosys.encrypt(pub, ht)         # r * g, H(t) * g + r * I
        return c, r

    def reencrypt_commitment(self, c):
        pub = self.elgamal_pub                          # I
        c_r, r_r = self._cryptosys.reencrypt(pub, c)    # (r1 + r2) * g, H(t) * g + (r1 + r2) * I
        return c_r, r_r

    def create_decryptor(self, r):
        pub = self.elgamal_pub                                  # I
        decryptor = self._cryptosys.create_decryptor(r, pub)    # r * I
        return decryptor

    def encrypt_decryptor(self, decryptor, verifier_pub):
        decryptor = self.encode(decryptor, 
            serializer=self.serialize_ecc_point)
        enc_decryptor = self.encrypt(
            decryptor,
            verifier_pub
        )                                               # E_V((r1 + r2) * I)
        return enc_decryptor

    def create_nirenc(self, c, c_r, r_r):
        pub = self.elgamal_pub
        nirenc = self._prover.prove_reencryption(c, c_r, r_r, pub)
        return nirenc

    def create_niddh(self, c_r, decryptor, r, r_r):
        pub = self.elgamal_pub
        niddh = self._prover.prove_decryption(c_r, decryptor, r + r_r, pub)
        return niddh

    def encrypt_niddh(self, niddh, verifier_pub):
        niddh = self.encode(niddh, serializer=self.serialize_niddh)
        enc_niddh = self.encrypt(niddh, verifier_pub)
        return enc_niddh

    def publish_award(self, title):
        title = title.encode('utf-8')                   # TODO
        c, r = self.commit_to_document(title)           # r * g, H(t) * g + r * I

        # Serialize output and create AWARD tag
        c = self.serialize_cipher(c)
        r = self.serialize_scalar(r)
        payload = self.create_tag(AWARD, c=c)
        s_awd = self.sign(payload)

        return s_awd, c, r

    def publish_proof(self, s_req, r, c, verifier_pub):

        # Deserialize input
        r = self.deserialize_scalar(r)
        c = self.deserialize_cipher(c)
        verifier_pub = self._key_manager.deserialize_public_shares(verifier_pub)

        c_r, r_r = self.reencrypt_commitment(c)         # (r + r_r) * g, H(t) * g + (r + r_r) * I

        decryptor = self.create_decryptor(r + r_r)      # (r + r_r) * I
        enc_decryptor = self.encrypt_decryptor(
            decryptor, verifier_pub)                    # E_V((r + r_r) * I)
        nirenc = self.create_nirenc(c, c_r, r_r)        # NIRENC_I(c, c_r)
        niddh = self.create_niddh(c_r, decryptor, 
            r, r_r)                                     # NIDDH_I(r + r_r)
        enc_niddh = self.encrypt_niddh(
            niddh, verifier_pub)                        # E_V(NIDDH_I(r + r_r))

        # Create proof and PROOF tag
        proof = set_proof(c_r, enc_decryptor, nirenc, enc_niddh)
        proof = self.serialize_proof(proof)
        payload = self.create_tag(PROOF, s_req=s_req, **proof)
        s_prf = self.sign(payload)

        return s_prf, proof


class Verifier(Party):

    def __init__(self, curve='P-384', key=None, hexifier=True, flattener=False):
        super().__init__(curve, key, hexifier=hexifier, flattener=flattener)
        self._verifier = _Verifier(curve)

    def _decrypt_decryptor(self, issuer_pub, enc_decryptor):
        decryptor = self.decrypt(enc_decryptor, issuer_pub)
        return self.decode(decryptor, self.deserialize_ecc_point)

    def _decrypt_niddh(self, issuer_pub, enc_niddh):
        niddh = self.decrypt(enc_niddh, issuer_pub)
        return self.decode(niddh, self.deserialize_niddh)

    def _retrieve_from_proof(self, issuer_pub, proof):
        proof = self.deserialize_proof(proof)
        c_r, enc_decryptor, nirenc, enc_niddh = extract_proof(proof)
        decryptor = self._decrypt_decryptor(issuer_pub, enc_decryptor)
        niddh = self._decrypt_niddh(issuer_pub, enc_niddh)
        return c_r, decryptor, nirenc, niddh

    def decrypt_commitment(self, c_r, decryptor):
        c_dec = self._cryptosys.decrypt_with_decryptor(c_r, decryptor)   # TODO
        return c_dec

    def verify_document_integrity(self, t, c_dec):
        return c_dec == self.hash_document(t)       # c_dec == H(t) * g?

    def verify_nirenc(self, nirenc, issuer_pub):
        pub = issuer_pub['ecc']
        return self._verifier.verify_ddh_proof(nirenc, pub)

    def verify_niddh(self, niddh, issuer_pub):
        pub = issuer_pub['ecc']
        return self._verifier.verify_ddh_proof(niddh, pub)

    def publish_ack(self, s_prf, title, proof, issuer_pub):
        title = title.encode('utf-8')                   # TODO
        issuer_pub = self._key_manager.deserialize_public_shares(issuer_pub)

        # Deserialize and decrypt (if needed) proof components
        c_r, decryptor, nirenc, niddh = self._retrieve_from_proof(
            issuer_pub, proof)

        # Decrypt the issuer's initial commitment to document
        c_dec = self.decrypt_commitment(c_r, decryptor)
    
        # Verifications
        check_integrity = self.verify_document_integrity(title, c_dec)
        check_nirenc    = self.verify_nirenc(nirenc, issuer_pub)
        check_niddh     = self.verify_niddh(niddh, issuer_pub)

        # Create result and ACK tag
        result = all((
            check_integrity, 
            check_nirenc, 
            check_niddh,
        ))
        assert result   # TODO: Remove
        payload = self.create_tag(ACK if result else NACK,
            s_prf=s_prf, result=result)
        s_ack = self.sign(payload)
        return s_ack, result
