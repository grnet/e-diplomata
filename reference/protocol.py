"""
Transaction Layer
"""

import json
from nacl.public import PrivateKey as _NaclKey
from nacl.public import PublicKey as _NaclPublicKey
from nacl.public import Box as _NaclBox
from elgamal import ElGamalCrypto, ElGamalSerializer, Signer, hash_into_scalar
from primitives import Prover as _Prover
from primitives import Verifier as _Verifier
from util import *

AWARD   = 'AWARD'
REQUEST = 'REQUEST'
PROOF   = 'PROOF'
ACK     = 'ACK'
NACK    = 'NACK'
FAIL    = 'FAIL'


class Party(ElGamalSerializer):
    """
    Common infrastructure for Holder, Issuer and Verifier
    """

    def __init__(self, curve='P-384'):
        self.cryptosys = ElGamalCrypto(curve)
        self.key = self._generate_keys(self.cryptosys)
        self._signer = self._create_signer(self.key)


    # Key management

    @staticmethod
    def _set_keys(ecc_key, nacl_key):
        return {
            'ecc': ecc_key,
            'nacl': nacl_key,
        }

    @staticmethod
    def _extract_keys(key):
        ecc_key  = key['ecc']
        nacl_key = key['nacl']
        return ecc_key, nacl_key

    @staticmethod
    def _extract_public_keys(key):
        ecc_pub  = key['ecc'].pointQ
        nacl_pub = key['nacl'].public_key
        return ecc_pub, nacl_pub

    def _generate_keys(self, cryptosys):
        ecc_key = cryptosys.generate_key()
        nacl_key = _NaclKey.generate()
        keys = self._set_keys(ecc_key, nacl_key)
        return keys

    def get_public_shares(self, serialized=True):
        ecc_pub, nacl_pub = self._extract_public_keys(self.key)
        if serialized:
            ecc_pub = self._serialize_ecc_public(ecc_pub)
            nacl_pub = self._serialize_nacl_public(nacl_pub)
        public_shares = self._set_keys(ecc_pub, nacl_pub)
        return public_shares

    def _get_ecc_keypair(self):
        ecc_key, _ = self._extract_keys(self.key)
        return ecc_key.d, ecc_key.pointQ

    @property
    def keys(self):
        ecc_key, nacl_key = self._extract_keys(self.key)
        return ecc_key, nacl_key

    @property
    def elgamal_key(self):
        ecc_key, _ = self.keys
        return ecc_key

    @property
    def public_keys(self):
        ecc_pub, nacl_pub = self._extract_public_keys(self.key)
        return ecc_pub, nacl_pub

    @property
    def elgamal_pub(self):
        ecc_pub, _ = self.public_keys
        return ecc_pub


    # Serialization/deserialization

    def _serialize_ecc_public(self, pub):
        return self._serialize_ecc_point(pub)

    def _deserialize_ecc_public(self, pub):
        return self._deserialize_ecc_point(pub)

    def _serialize_nacl_public(self, pub):
        return bytes(pub).hex()

    def _deserialize_nacl_public(self, pub):
        return _NaclPublicKey(bytes.fromhex(pub))

    def _deserialize_public(self, public):
        ecc_pub, nacl_pub = self._extract_keys(public)
        ecc_pub = self._deserialize_ecc_public(ecc_pub)
        nacl_pub = self._deserialize_nacl_public(nacl_pub)
        public = self._set_keys(ecc_pub, nacl_pub)
        return public

    def _serialize_nirenc(self, nirenc):
        proof_c1, proof_c2 = extract_nirenc(nirenc)
        proof_c1 = self._serialize_ddh_proof(proof_c1)
        proof_c2 = self._serialize_ddh_proof(proof_c2)
        nirenc = set_nirenc(proof_c1, proof_c2)
        return nirenc

    def _deserialize_nirenc(self, nirenc):
        proof_c1, proof_c2 = extract_nirenc(nirenc)
        proof_c1 = self._deserialize_ddh_proof(proof_c1)
        proof_c2 = self._deserialize_ddh_proof(proof_c2)
        nirenc = set_nirenc(proof_c1, proof_c2)
        return nirenc

    def _serialize_niddh(self, niddh):
        return self.cryptosys.serialize_ddh_proof(niddh)

    def _deserialize_niddh(self, niddh):
        return self.cryptosys.deserialize_ddh_proof(niddh)


    # Encoding for symmetric encryption

    def encode(self, entity, serializer):
        return json.dumps(serializer(
            entity)).encode('utf-8')

    def decode(self, entity, deserializer):
        return deserializer(json.loads(
            entity.decode('utf-8')))


    # Symmetrict encryption

    def encrypt(self, content, receiver_pub):
        """
        Encrypt using common secret
        """
        box = _NaclBox(self.key['nacl'], receiver_pub['nacl'])
        cipher = box.encrypt(content).hex()
        return cipher

    def decrypt(self, cipher, sender_pub):
        """
        Decrypt using common secret
        """
        box = _NaclBox(self.key['nacl'], sender_pub['nacl'])
        content = box.decrypt(bytes.fromhex(cipher))
        return content


    # Tag creation

    @staticmethod
    def create_tag(label, *args, **kwargs):
        out = label
        for arg in args:
            out += f' {arg}'
        for (key, value) in kwargs.items():
            out += f' {key}={value}'
        return out.encode('utf-8')


    # Signatures

    @staticmethod
    def _create_signer(key):
        return Signer(key['ecc'])

    def sign(self, payload):
        return self._signer.sign(payload).hex()

    def verify_signature(self, sig):
        s = bytes.fromhex(sig)
        return self._signer.verify_signature(sig)


class Holder(Party):

    def __init__(self, curve='P-386'):
        super().__init__(curve)

    def publish_request(self, s_awd, verifier_pub):
        pub = verifier_pub['ecc']
        payload = self.create_tag(REQUEST, s_awd=s_awd, ver_pub=pub)
        s_req = self.sign(payload)
        return s_req


class Issuer(Party):

    def __init__(self, curve='P-386'):
        super().__init__(curve)
        self._prover = _Prover(curve, key=self.elgamal_key)

    def commit_to_document(self, t):
        ht = hash_into_scalar(t)                        # H(t)
        pub = self.elgamal_pub                          # I
        c, r = self._prover.commit(ht, pub=pub)         # r * g, H(t) * g + r * I
        return c, r

    def reencrypt_commitment(self, c):
        pub = self.elgamal_pub                          # I
        c_r, r_r = self._prover.reencrypt(pub, c)       # (r1 + r2) * g, H(t) * g + (r1 + r2) * I
        return c_r, r_r

    def create_decryptor(self, r1, r2):
        pub = self.elgamal_pub                          # I
        decryptor = self._prover.generate_decryptor(
            r1, r2, pub)
        return decryptor                                # (r1 + r2) * I

    def encrypt_decryptor(self, decryptor, verifier_pub):
        decryptor = self.encode(decryptor, 
            serializer=self._serialize_ecc_point)
        enc_decryptor = self.encrypt(
            decryptor,
            verifier_pub
        )                                               # E_V((r1 + r2) * I)
        return enc_decryptor

    def create_nirenc(self, c, c_r):
        keypair = self._get_ecc_keypair()
        return self._prover.generate_nirenc(c, c_r, keypair)

    def create_niddh(self, r1, r2):
        keypair = self._get_ecc_keypair()
        return self._prover.generate_niddh(r1, r2, keypair)

    def encrypt_niddh(self, niddh, verifier_pub):
        niddh = self.encode(niddh, 
            serializer=self._serialize_niddh)
        enc_niddh = self.encrypt(niddh, verifier_pub)
        return enc_niddh

    def publish_award(self, t):
        c, r = self.commit_to_document(t)               # r * g, H(t) * g + r * I

        # Serialize output and create AWARD tag
        c = self._serialize_cipher(c)
        r = self._serialize_scalar(r)
        payload = self.create_tag(AWARD, c=c)
        s_awd = self.sign(payload)

        return s_awd, c, r

    def publish_proof(self, s_req, r, c, verifier_pub):

        # Deserialize input
        r = self._deserialize_scalar(r)
        c = self._deserialize_cipher(c)
        verifier_pub = self._deserialize_public(verifier_pub)

        c_r, r_r = self.reencrypt_commitment(c)         # (r + r_r) * g, H(t) * g + (r + r_r) * I

        # Create reencryption-decryptor
        decryptor = self.create_decryptor(r, r_r)       # (r + r_r) * I

        # Create NIRENC for c, c_r
        nirenc = self.create_nirenc(c, c_r)             # NIRENC_I(c, c_r)

        # Create NIDDH for reencryption-decryptor
        niddh = self.create_niddh(r, r_r)               # NIDDH_I(r + r_r)

        # Create proof and PROOF tag
        c_r = self._serialize_cipher(c_r)               # c_r
        enc_decryptor = self.encrypt_decryptor(
            decryptor, verifier_pub)                    # E_V((r + r_r) * I)
        nirenc = self._serialize_nirenc(nirenc)         # NIRENC_I(c, c_r)
        enc_niddh = self.encrypt_niddh(
            niddh, verifier_pub)                        # E_V(NIDDH_I(r + r_r))
        proof = set_proof(c_r, enc_decryptor, nirenc, enc_niddh)
        payload = self.create_tag(PROOF, s_req=s_req, **proof)
        s_prf = self.sign(payload)

        return s_prf, proof


class Verifier(Party):

    def __init__(self, curve='P-386'):
        super().__init__(curve)
        self._verifier = _Verifier(curve, key=self.elgamal_key)

    def _retrieve_decryptor(self, issuer_pub, enc_decryptor):
        decryptor = self.decrypt(enc_decryptor, issuer_pub)
        return self.decode(decryptor, self._deserialize_ecc_point)

    def _retrieve_niddh(self, issuer_pub, enc_niddh):
        niddh = self.decrypt(enc_niddh, issuer_pub)
        return self.decode(niddh, self._deserialize_niddh)

    def _retrieve_from_proof(self, issuer_pub, proof):
        c_r, enc_decryptor, nirenc, enc_niddh = extract_proof(proof)
        c_r = self._deserialize_cipher(c_r)
        decryptor = self._retrieve_decryptor(issuer_pub, enc_decryptor)
        nirenc = self._deserialize_nirenc(nirenc)
        niddh = self._retrieve_niddh(issuer_pub, enc_niddh)
        return c_r, decryptor, nirenc, niddh

    def decrypt_commitment(self, c_r, decryptor):
        c = self.cryptosys.drenc(c_r, decryptor)    # TODO
        return c

    def verify_document_integrity(self, t, c):
        ht = hash_into_scalar(t)
        return self._verifier.verify_message_integrity(ht, c)

    def verify_nirenc(self, nirenc, issuer_pub):
        pub = issuer_pub['ecc']
        return self._verifier.verify_nirenc(nirenc, pub)

    def verify_niddh(self, niddh, issuer_pub):
        pub = issuer_pub['ecc']
        return self._verifier.verify_niddh(niddh, pub)

    def publish_ack(self, s_prf, t, proof, issuer_pub):
        issuer_pub = self._deserialize_public(issuer_pub)

        # Deserialize and decrypt (if needed) proof components
        c_r, decryptor, nirenc, niddh = self._retrieve_from_proof(
            issuer_pub, proof)

        # Retrieve the issuer's initial commitment to document
        c = self.decrypt_commitment(c_r, decryptor)
    
        # Verifications
        check_integrity = self.verify_document_integrity(t, c)
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
