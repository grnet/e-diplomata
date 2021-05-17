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

    # @staticmethod
    def _generate_keys(self, cryptosys):
        ecc_key = cryptosys.generate_key()
        nacl_key = PrivateKey.generate()
        keys = self._set_keys(ecc_key, nacl_key)
        return keys

    def get_public_shares(self, serialized=True):
        ecc_key, nacl_key = self._extract_keys(self.key)
        ecc_pub = ecc_key.pointQ                                        # TODO
        nacl_pub = nacl_key.public_key                                  # TODO
        if serialized:
            ecc_pub = self.cryptosys.serialize_ecc_point(ecc_pub)       # TODO
            nacl_pub = bytes(nacl_pub).hex()                            # TODO
        public_shares = self._set_keys(ecc_pub, nacl_pub)
        return public_shares

    @property
    def keys(self):
        ecc_key, nacl_key = self._extract_keys(self.key)
        return ecc_key, nacl_key

    @property
    def public_keys(self):
        public_shares = self.get_public_shares(serialized=False)
        ecc_pub, nacl_pub = self._extract_keys(public_shares)
        return ecc_pub, nacl_pub

    def deserialize_public(self, public):
        ecc_pub, nacl_pub = self._extract_keys(public)
        ecc_pub = self.cryptosys.deserialize_ecc_point(ecc_pub)         # TODO
        nacl_pub = PublicKey(bytes.fromhex(nacl_pub))                   # TODO
        public = self._set_keys(ecc_pub, nacl_pub)
        return public


    # Symmetrict encryption

    def encrypt(self, content, receiver_pub):
        """
        Encrypt using common secret (currently a wrapper around box.encrypt)
        """
        box = Box(self.key['nacl'], receiver_pub['nacl'])
        cipher = box.encrypt(content)
        return cipher

    def decrypt(self, cipher, sender_pub):
        """
        Decrypt using common secret (currently a wrapper around box.decrypt)
        """
        box = Box(self.key['nacl'], sender_pub['nacl'])
        content = box.decrypt(cipher)
        return content


    # Signatures

    @staticmethod
    def _create_signer(key):
        return Signer(key['ecc'])

    def sign(self, payload):
        return self.signer.sign(payload)

    def verify_signature(self, s):
        return self.signer.verify_signature(s)


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

    def commit_to_document(self, document):
        ecc_pub, _ = self.public_keys
        return self.prover.commit(ecc_pub, document)                    # TODO

    def reencrypt_commitment(self, c):
        ecc_pub, _ = self.public_keys
        c_r, r_r = self.prover.reencrypt(ecc_pub, c)                    # TODO
        return c_r, r_r

    def create_decryptor(self, r1, r2, verifier_pub):
        r_tilde = r1 + r2
        pub, _ = self.public_keys
        decryptor =  r_tilde * pub              # TODO

        # TODO: Separate encryption from generation
        enc_decryptor = self.encrypt(
            str(decryptor.xy).encode('utf-8'),  # TODO
            verifier_pub
        )

        return decryptor, enc_decryptor

    def _serialize_nirenc(self, nirenc):
        proof_c1, proof_c2 = extract_nirenc(nirenc)
        proof_c1 = self.prover._serialize_ddh_proof(proof_c1)       # TODO
        proof_c2 = self.prover._serialize_ddh_proof(proof_c2)       # TODO
        nirenc = set_nirenc(proof_c1, proof_c2)
        return nirenc

    def publish_award(self, t):
        c, r = self.commit_to_document(t)   # (c1, c2), r

        c1, c2 = extract_cipher(c)
        payload = f'AWARD c1={c1.xy} c2={c2.xy}'.encode('utf-8')

        s_awd = self.sign(payload)

        c = self.cryptosys.serialize_cipher(c)                      # TODO
        r = self.cryptosys.serialize_scalar(r)                      # TODO
        return s_awd, c, r


    def publish_proof(self, r, c, s_req, verifier_pub):

        r = self.cryptosys.deserialize_scalar(r)                    # TODO
        c = self.cryptosys.deserialize_cipher(c)                    # TODO


        # import pdb; pdb.set_trace()
        verifier_pub = self.deserialize_public(verifier_pub)

        # Re-encrypt commitment
        c_r, r_r = self.reencrypt_commitment(c)

        # Create and encrypt decryptor
        # TODO: separate generation from encryption
        decryptor, enc_decryptor = self.create_decryptor(r, r_r, verifier_pub)
        enc_decryptor = enc_decryptor.hex()                         # TODO

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
        enc_niddh = enc_niddh.hex()     # TODO

        # Create PROOF tag
        nirenc_str = json.dumps(nirenc)
        c_r_1, c_r_2 = extract_cipher(c_r)
        payload = (f'PROOF s_req={s_req} c_r=({c_r_1.xy, c_r_2.xy}) '
                   f'{nirenc_str} {enc_decryptor} '
                   f'{enc_niddh}'.encode('utf-8'))
        s_prf = self.sign(payload)

        c_r = self.cryptosys.serialize_cipher(c_r)              # TODO

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
        decryptor = self.verifier._deserialize_ecc_point((x_affine, y_affine)) # TODO
        return decryptor

    def _deserialize_nirenc(self, nirenc):
        proof_c1, proof_c2 = extract_nirenc(nirenc)
        proof_c1 = self.verifier._deserialize_ddh_proof(proof_c1)   # TODO
        proof_c2 = self.verifier._deserialize_ddh_proof(proof_c2)   # TODO
        nirenc = set_nirenc(proof_c1, proof_c2)
        return nirenc

    def publish_ack(self, s_prf, m, c_r, nirenc, enc_decryptor, enc_niddh, issuer_pub):
        c_r = self.cryptosys.deserialize_cipher(c_r)
        issuer_pub = self.deserialize_public(issuer_pub)

        # VERIFIER etrieves decryptor created for them by ISSUER
        enc_decryptor = bytes.fromhex(enc_decryptor)
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
        enc_niddh = bytes.fromhex(enc_niddh)
        niddh = json.loads(self.decrypt(enc_niddh, issuer_pub).decode('utf-8')) # TODO
        niddh = self.verifier._deserialize_ddh_proof(niddh)                     # TODO
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
