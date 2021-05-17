import json
import re
from nacl.public import PrivateKey, Box
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
        self.key = self._generate_key(self.cryptosys)
        self.signer = Signer(self.key['ecc'])


    @staticmethod
    def _generate_key(cryptosys):
        key = {
            'ecc': cryptosys.generate_key(),
            'nacl': PrivateKey.generate(),
        }
        return key

    def get_public_shares(self):
        return {
            'ecc': self.key['ecc'].pointQ,
            'nacl': self.key['nacl'].public_key,
        }


    # Symmetrict encryption

    def encrypt(self, content, receiver_pub):
        """
        Encrypt using common secret (currently a wrapper around box.encrypt)

        content: bytes
        """
        box = Box(self.key['nacl'], receiver_pub['nacl'])
        cipher = box.encrypt(content)
        return cipher

    def decrypt(self, cipher, sender_pub):
        """
        Decrypt using common secret (currently a wrapper around box.decrypt)

        return: bytes
        """
        box = Box(self.key['nacl'], sender_pub['nacl'])
        content = box.decrypt(cipher)
        return content


    # Signatures

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
        self.prover = primitives.Prover(curve, key=self.key['ecc'])    # TODO

    def commit_to_document(self, document):
        return self.prover.commit(              # TODO
            self.get_public_shares()['ecc'],           # TODO
            document
        )

    def reencrypt_commitment(self, c):
        c_r, r_r = self.prover.reencrypt(       # TODO
            self.get_public_shares()['ecc'],           # TODO
            c,
        )
        return c_r, r_r

    def create_decryptor(self, r1, r2, verifier_pub):
        r_tilde = r1 + r2
        pub = self.get_public_shares()['ecc']   # TODO
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
        return s_awd, c, r


    def publish_proof(self, r, c, s_req, verifier_pub):

        # Re-encrypt commitment
        c_r, r_r = self.reencrypt_commitment(c)

        # Create and encrypt decryptor
        # TODO: separate generation from decryption
        decryptor, enc_decryptor = self.create_decryptor(r, r_r, verifier_pub)

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

        return (s_prf, c_r, nirenc, enc_decryptor, enc_niddh)


class Verifier(Party):

    def __init__(self, curve='P-386'):
        super().__init__(curve)
        self.verifier = primitives.Verifier(curve, key=self.key['ecc'])    # TODO

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
