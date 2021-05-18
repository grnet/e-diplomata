import json
import re
from nacl.public import PrivateKey, PublicKey, Box
from Cryptodome.Signature import DSS
from Cryptodome.Hash import SHA384
from crypto import ElGamalCrypto, ElGamalWrapper
from structs import *
from util import hash_into_integer
from primitives import *
import primitives


class Party(object):

    def __init__(self, curve='P-384'):
        self.cryptosys = ElGamalCrypto(curve)
        self.key = self._generate_keys(self.cryptosys)
        self.signer = self._create_signer(self.key)


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

    # @staticmethod
    def _generate_keys(self, cryptosys):
        ecc_key = cryptosys.generate_key()
        nacl_key = PrivateKey.generate()
        keys = self._set_keys(ecc_key, nacl_key)
        return keys

    def get_public_shares(self, serialized=True):
        ecc_pub, nacl_pub = self._extract_public_keys(self.key)
        if serialized:
            ecc_pub = self._serialize_ecc_public(ecc_pub)
            nacl_pub = self._serialize_nacl_public(nacl_pub)
        public_shares = self._set_keys(ecc_pub, nacl_pub)
        return public_shares

    @property
    def keys(self):
        ecc_key, nacl_key = self._extract_keys(self.key)
        return ecc_key, nacl_key

    @property
    def public_keys(self):
        ecc_pub, nacl_pub = self._extract_public_keys(self.key)
        return ecc_pub, nacl_pub


    # Serialization/deserialization

    def _serialize_scalar(self, scalar):
        return self.cryptosys.serialize_scalar(scalar)

    def _deserialize_scalar(self, scalar):
        return self.cryptosys.deserialize_scalar(scalar)

    def _serialize_ecc_point(self, pt):
        return self.cryptosys.serialize_ecc_point(pt)

    def _deserialize_ecc_point(self, pt):
        return self.cryptosys.deserialize_ecc_point(pt)

    def _serialize_cipher(self, cipher):
        return self.cryptosys.serialize_cipher(cipher)

    def _deserialize_cipher(self, cipher):
        return self.cryptosys.deserialize_cipher(cipher)

    def _serialize_ddh_proof(self, ddh_proof):
        return self.cryptosys.serialize_ddh_proof(ddh_proof)

    def _deserialize_ddh_proof(self, ddh_proof):
        return self.cryptosys.deserialize_ddh_proof(ddh_proof)

    def _serialize_ecc_public(self, pub):
        return self._serialize_ecc_point(pub)

    def _deserialize_ecc_public(self, pub):
        return self._deserialize_ecc_point(pub)

    def _serialize_nacl_public(self, pub):
        return bytes(pub).hex()

    def _deserialize_nacl_public(self, pub):
        return PublicKey(bytes.fromhex(pub))

    def deserialize_public(self, public):
        ecc_pub, nacl_pub = self._extract_keys(public)
        ecc_pub = self._deserialize_ecc_public(ecc_pub)
        nacl_pub = self._deserialize_nacl_public(nacl_pub)
        public = self._set_keys(ecc_pub, nacl_pub)
        return public


    # Symmetrict encryption

    def encrypt(self, content, receiver_pub):
        """
        Encrypt using common secret (currently a wrapper around box.encrypt)
        """
        box = Box(self.key['nacl'], receiver_pub['nacl'])
        cipher = box.encrypt(content).hex()
        return cipher

    def decrypt(self, cipher, sender_pub):
        """
        Decrypt using common secret (currently a wrapper around box.decrypt)
        """
        box = Box(self.key['nacl'], sender_pub['nacl'])
        content = box.decrypt(bytes.fromhex(cipher))
        return content


    # Signatures

    @staticmethod
    def _create_signer(key):
        return Signer(key['ecc'])

    def sign(self, payload):
        return self.signer.sign(payload).hex()

    def verify_signature(self, sig):
        s = bytes.fromhex(sig)
        return self.signer.verify_signature(sig)


class Holder(Party):

    def __init__(self, curve='P-386'):
        super().__init__(curve)

    def publish_request(self, s_awd, verifier_pub):
        pub = verifier_pub['ecc']
        payload = (f'REQUEST s_awd={s_awd} ver_pub={pub}').encode('utf-8')
        s_req = self.sign(payload)
        return s_req


class Issuer(Party):

    def __init__(self, curve='P-386'):
        super().__init__(curve)
        ecc_key, _ = self.keys
        self.prover = primitives.Prover(curve, key=ecc_key)     # TODO

    def commit_to_document(self, t):
        ht = hash_into_integer(t)                       # H(t)
        ecc_pub, _ = self.public_keys                   # I
        c, r = self.prover.commit(ht, pub=ecc_pub)      # r * g, H(t) * g + r * I
        return c, r

    def reencrypt_commitment(self, c):
        ecc_pub, _ = self.public_keys                   # I
        c_r, r_r = self.prover.reencrypt(ecc_pub, c)    # (r1 + r2) * g, H(t) * g + (r1 + r2) * I
        return c_r, r_r

    def create_decryptor(self, r1, r2):
        ecc_pub, _ = self.public_keys                   # I
        decryptor = self.prover.generate_decryptor(
            r1, r2, ecc_pub)
        return decryptor                                # (r1 + r2) * I

    def encrypt_decryptor(self, decryptor, verifier_pub):
        return self.encrypt(
            str(decryptor.xy).encode('utf-8'),  # TODO
            verifier_pub
        )                                               # E_V((r1 + r2) * I)

    def _serialize_nirenc(self, nirenc):
        proof_c1, proof_c2 = extract_nirenc(nirenc)
        proof_c1 = self._serialize_ddh_proof(proof_c1)       # TODO
        proof_c2 = self._serialize_ddh_proof(proof_c2)       # TODO
        nirenc = set_nirenc(proof_c1, proof_c2)
        return nirenc

    def publish_award(self, t):
        c, r = self.commit_to_document(t)               # r * g, H(t) * g + r * I

        c1, c2 = extract_cipher(c)
        payload = f'AWARD c1={c1.xy} c2={c2.xy}'.encode('utf-8')    # TODO

        s_awd = self.sign(payload)

        c = self._serialize_cipher(c)                      # TODO
        r = self._serialize_scalar(r)                      # TODO
        return s_awd, c, r


    def publish_proof(self, r, c, s_req, verifier_pub):
        r = self._deserialize_scalar(r)                         # TODO
        c = self._deserialize_cipher(c)                         # TODO
        verifier_pub = self.deserialize_public(verifier_pub)    # TODO

        # Re-encrypt commitment
        c_r, r_r = self.reencrypt_commitment(c)         # (r + r_r) * g, H(t) * g + (r + r_r) * I

        # Create and encrypt reencryption-decryptor
        decryptor = self.create_decryptor(r, r_r)       # (r + r_r) * I
        enc_decryptor = self.encrypt_decryptor(
            decryptor, verifier_pub)                    # E_V((r + r_r) * I)

        # create NIRENC
        # TODO serapate generation from serialization
        nirenc = self.prover.generate_nirenc(c, c_r, verifier_pub)
        nirenc = self._serialize_nirenc(nirenc)

        # Create and encrypt NIDDH of the above decryptor addressed to VERIFIER
        # TODO: Separate generation from encryption
        niddh = self.prover.generate_niddh(r, r_r, verifier_pub)
        enc_niddh = self.encrypt(
            json.dumps(niddh).encode('utf-8'),
            verifier_pub
        )

        # Create PROOF tag
        nirenc_str = json.dumps(nirenc)
        c_r_1, c_r_2 = extract_cipher(c_r)
        payload = (f'PROOF s_req={s_req} c_r=({c_r_1.xy, c_r_2.xy}) '
                   f'{nirenc_str} {enc_decryptor} '
                   f'{enc_niddh}'.encode('utf-8'))
        s_prf = self.sign(payload)

        c_r = self._serialize_cipher(c_r)              # TODO

        return (s_prf, c_r, nirenc, enc_decryptor, enc_niddh)


class Verifier(Party):

    def __init__(self, curve='P-386'):
        super().__init__(curve)
        ecc_key, _ = self.keys
        self.verifier = primitives.Verifier(curve, key=ecc_key)    # TODO

    def retrieve_decryptor(self, sender_pub, enc_decryptor):
        dec_decryptor = self.decrypt(enc_decryptor, sender_pub).decode('utf-8')

        # TODO
        extract_coords = re.match(r'^\D*(\d+)\D+(\d+)\D*$', dec_decryptor)
        x_affine = int(extract_coords.group(1))
        y_affine = int(extract_coords.group(2))
        # TODO: Raise exception for caller?
        if not extract_coords:
            payload = f'FAIL {s_prf}'.encode('utf-8')
            s_ack = verifier.sign(payload)
            return s_ack
        decryptor = self._deserialize_ecc_point((x_affine, y_affine)) # TODO
        return decryptor

    def _deserialize_nirenc(self, nirenc):
        proof_c1, proof_c2 = extract_nirenc(nirenc)
        proof_c1 = self._deserialize_ddh_proof(proof_c1)   # TODO
        proof_c2 = self._deserialize_ddh_proof(proof_c2)   # TODO
        nirenc = set_nirenc(proof_c1, proof_c2)
        return nirenc

    def publish_ack(self, s_prf, m, c_r, nirenc, enc_decryptor, enc_niddh, issuer_pub):
        c_r = self._deserialize_cipher(c_r)
        issuer_pub = self.deserialize_public(issuer_pub)

        # VERIFIER etrieves decryptor created for them by ISSUER
        decryptor = self.retrieve_decryptor(issuer_pub, enc_decryptor)
    
        # VERIFIER decrypts the re-encrypted commitment
        dec_m = self.verifier.decrypt_commitment(c_r, decryptor)    # TODO
    
        # VERIFIER checks content of document
        check_m_integrity = self.verifier.check_message_integrity(m, dec_m) # TODO
        assert check_m_integrity    # TODO: Remove
    
        # VERIFIER verifies NIRENC proof
        nirenc = self._deserialize_nirenc(nirenc)
        check_nirenc = self.verifier.verify_nirenc(nirenc, issuer_pub)      # TODO
        assert check_nirenc         # TODO: Remove
    
        # VERIFIER verifies NIDDH proof
        niddh = json.loads(self.decrypt(enc_niddh, issuer_pub).decode('utf-8')) # TODO
        niddh = self._deserialize_ddh_proof(niddh)                     # TODO
        check_niddh = self.verifier.verify_niddh(niddh, issuer_pub)
        assert check_niddh          # TODO: Remove
    
        # VERIFIER creates TAG
        if not all((
            check_m_integrity, 
            check_nirenc, 
            check_niddh,
        )):
            # Some check failed; reject proof
            payload = f'FAIL {s_prf}'.encode('utf-8')
            s_ack = self.sign(payload)
            return s_ack
        else:
            # All checks succeded, acknowledge proof
            payload = f'ACK {s_prf}'.encode('utf-8')
            s_ack = self.sign(payload)
            return s_ack
