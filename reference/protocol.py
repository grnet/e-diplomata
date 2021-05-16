import json
import re
from nacl.public import PrivateKey, Box
from Cryptodome.Signature import DSS
from Cryptodome.Hash import SHA384
from crypto import ElGamalCrypto
from util import hash_into_integer


class Party(object):

    def __init__(self, curve='P-384'):
        self.cryptosys = ElGamalCrypto(curve)
        self.key = self._generate_key(self.cryptosys)
        self.signer = self._create_signer(self.key['ecc'])

    @property
    def generator(self):
        return self.cryptosys.generator


    # Key management

    @staticmethod
    def _generate_key(cryptosys):
        key = {
            'ecc': cryptosys.generate_key(),
            'nacl': PrivateKey.generate(),
        }
        return key

    @property
    def private(self):
        return self.key['ecc'].d

    @property
    def public(self):
        return self.key['ecc'].pointQ

    @property
    def elgamal_key(self):
        return self.private, self.public

    def get_public_shares(self):
        return {
            'ecc': self.key['ecc'].pointQ,
            'nacl': self.key['nacl'].public_key,
        }


    # Symmetric encryption

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


    # DSA (Digital Signature Algorithm)

    @staticmethod
    def _create_signer(key):
        return DSS.new(key, 'fips-186-3')

    def sign(self, payload):
        hc = SHA384.new(payload)
        signature = self.signer.sign(hc)
        return signature

    def verify_signature(self, s):
        pass


    # ElGamal structures

    def _serialize_ecc_point(self, pt):
        return self.cryptosys.serialize_ecc_point(pt)
    
    def _deserialize_ecc_point(self, pt):
        return self.cryptosys.deserialize_ecc_point(pt)
    
    def _serialize_factor(self, factor):
        return self.cryptosys.serialize_factor(factor)
    
    def _deserialize_factor(self, factor):
        return self.cryptosys.deserialize_factor(factor)

    def _set_cipher(self, c1, c2):
        return self.cryptosys.set_cipher(c1, c2)
    
    def _extract_cipher(self, cipher):
        return self.cryptosys.extract_cipher(cipher)

    def _serialize_ddh(self, ddh):
        return self.cryptosys.serialize_ddh(ddh)
    
    def _deserialize_ddh(self, ddh):
        return self.cryptosys.deserialize_ddh(ddh)

    def _set_proof(self, u_comm, v_comm, s, d):
        return self.cryptosys.set_proof(u_comm, v_comm, s, d)

    def _extract_proof(self, proof):
        return self.cryptosys.extract_proof(proof)

    def _serialize_proof(self, proof):
        return self.cryptosys.serialize_proof(proof)
    
    def _deserialize_proof(self, proof):
        return self.cryptosys.deserialize_proof(proof)
    
    def _set_ddh_proof(self, ddh, proof):
        return self.cryptosys.set_ddh_proof(ddh, proof)
    
    def _extract_ddh_proof(self, ddh_proof):
        return self.cryptosys.extract_ddh_proof(ddh_proof)

    def _serialize_ddh_proof(self, ddh_proof):
        return self.cryptosys.serialize_ddh_proof(ddh_proof)
    
    def _deserialize_ddh_proof(self, ddh_proof):
        return self.cryptosys.deserialize_ddh_proof(ddh_proof)

    def _set_nirenc(self, proof_c1, proof_c2):
        return {
            'proof_c1': proof_c1,
            'proof_c2': proof_c2,
        }

    def _extract_nirenc(self, nirenc):
        proof_c1 = nirenc['proof_c1']
        proof_c2 = nirenc['proof_c2']
        return proof_c1, proof_c2

    def _serialize_nirenc(self, nirenc):
        proof_c1, proof_c2 = self._extract_nirenc(nirenc)
        proof_c1 = self._serialize_ddh_proof(proof_c1)
        proof_c2 = self._serialize_ddh_proof(proof_c2)
        nirenc = self._set_nirenc(proof_c1, proof_c2)
        return nirenc

    def _deserialize_nirenc(self, nirenc):
        proof_c1, proof_c2 = self._extract_nirenc(nirenc)
        proof_c1 = self._deserialize_ddh_proof(proof_c1)
        proof_c2 = self._deserialize_ddh_proof(proof_c2)
        nirenc = self._set_nirenc(proof_c1, proof_c2)
        return nirenc


    # ElGamal encryption
 
    def elgamal_encrypt(self, public, m):
        pub = public['ecc']
        return self.cryptosys.encrypt(pub, m)

    def elgamal_decrypt(self, cipher, table):
        priv = self.private
        return self.cryptosys.decrypt(priv, cipher, table)

    def elgamal_reencrypt(self, public, cipher):    
        pub = public['ecc']
        cipher, r = self.cryptosys.reencrypt(pub, cipher)
        return cipher, r
    
    def elgamal_drenc(self, cipher, decryptor):
        return self.cryptosys.drenc(cipher, decryptor)

    # TODO: Make clear the meaning of this function with respet to ElGamal
    # encryption and rename appropriately
    def commit(self, public, t):
        ht = hash_into_integer(t)                   # H(t)
        c, r = self.elgamal_encrypt(public, ht)     # (r * g, H(t) * g + r * I), r
        return c, r
    

    # Chaum-Pedersen protocol

    def _generate_chaum_pedersen(self, ddh, z, *extras):
        return self.cryptosys.generate_chaum_pedersen(ddh, z, *extras)
    
    def _verify_chaum_pedersen(self, ddh, proof, *extras):
        return self.cryptosys.verify_chaum_pedersen(ddh, proof, *extras)


class Holder(Party):

    def publish_request(self, s_awd, verifier_pub):
        pub = verifier_pub['ecc']
        payload = (f'REQUEST s_awd={s_awd} ver_pub={pub}').encode('utf-8')
        s_req = self.sign(payload)
        return s_req


class Issuer(Party):

    def commit_to_document(self, document):
        return self.commit(
            self.get_public_shares(),           # TODO
            document
        )

    def publish_award(self, t):
        c, r = self.commit_to_document(t)   # (c1, c2), r

        c1, c2 = self._extract_cipher(c)
        payload = f'AWARD c1={c1.xy} c2={c2.xy}'.encode('utf-8')

        s_awd = self.sign(payload)
        return s_awd, c, r

    def reencrypt_commitment(self, c):
        c_r, r_r = self.elgamal_reencrypt(
            self.get_public_shares(),           # TODO
            c,
        )
        return c_r, r_r

    def create_decryptor(self, r1, r2, verifier_pub):
        r_tilde = r1 + r2
        pub = self.public
        decryptor =  r_tilde * pub              # TODO

        enc_decryptor = self.encrypt(
            str(decryptor.xy).encode('utf-8'),
            verifier_pub
        )

        return decryptor, enc_decryptor

    def generate_nirenc(self, c, c_r, verifier_pub):
        c1  , c2   = self._extract_cipher(c)
        c1_r, c2_r = self._extract_cipher(c_r)

        priv, pub = self.elgamal_key
        extras = (pub,)

        # TODO:
        proof_c1 = self._set_ddh_proof(
            (c1, pub, c1_r),
            self._generate_chaum_pedersen((c1, pub, c1_r), priv, *extras)
        )
        proof_c2 = self._set_ddh_proof(
            (c2, pub, c2_r),
            self._generate_chaum_pedersen((c2, pub, c2_r), priv, *extras)
        )

        nirenc = self._set_nirenc(proof_c1, proof_c2)
        return nirenc

    def generate_niddh(self, r1, r2, verifier_pub):
        g = self.generator

        g_r   = r1 * g
        g_r_r = r2 * g

        priv, pub = self.elgamal_key
        extras = (pub,)

        # TODO
        niddh = self._set_ddh_proof(
            (g_r, pub, g_r_r),
            self._generate_chaum_pedersen((g_r, pub, g_r_r), priv, *extras)
        )
        niddh = self._serialize_ddh_proof(niddh)

        enc_niddh = self.encrypt(
            json.dumps(niddh).encode('utf-8'),
            verifier_pub
        )
        return niddh, enc_niddh


    def publish_proof(self, r, c, s_req, verifier_pub):
        # Re-encrypt commitment
        c_r, r_r = self.reencrypt_commitment(c)

        # Create and encrypt decryptor
        decryptor, enc_decryptor = self.create_decryptor(r, r_r, verifier_pub)

        # create NIRENC
        nirenc = self.generate_nirenc(c, c_r, verifier_pub)
        nirenc = self._serialize_nirenc(nirenc)

        # Create and encrypt NIDDH of the above decryptor addressed to VERIFIER
        niddh, enc_niddh = self.generate_niddh(r, r_r, verifier_pub)

        # Create PROOF tag
        nirenc_str = json.dumps(nirenc)
        c_r_1, c_r_2 = self._extract_cipher(c_r)
        payload = (f'PROOF s_req={s_req} c_r=({c_r_1.xy, c_r_2.xy}) '
                   f'{nirenc_str} {enc_decryptor} '
                   f'{enc_niddh}'.encode('utf-8'))
        s_prf = self.sign(payload)

        return (s_prf, c_r, nirenc, enc_decryptor, enc_niddh)


class Verifier(Party):

    def retrieve_decryptor(self, issuer_pub, enc_decryptor):
        dec_decryptor = self.decrypt(enc_decryptor, issuer_pub).decode('utf-8')

        # TODO
        extract_coords = re.match(r'^\D*(\d+)\D+(\d+)\D*$', dec_decryptor)
        x_affine = int(extract_coords.group(1))
        y_affine = int(extract_coords.group(2))
        # TODO: Raise exception for caller?
        if not extract_coords:
            payload = f'FAIL {s_prf}'.encode('utf-8')
            s_ack = verifier.sign(payload)
            return s_ack
        decryptor = self._deserialize_ecc_point((x_affine, y_affine))
        return decryptor

    def decrypt_commitment(self, c_r, decryptor):
        dec_m = self.elgamal_drenc(c_r, decryptor)
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

        nirenc = self._deserialize_nirenc(nirenc)
        proof_c1, proof_c2 = self._extract_nirenc(nirenc)
        extras = (issuer_pub['ecc'],)

        ddh, proof = self._extract_ddh_proof(proof_c1)
        check_proof_c1 = self._verify_chaum_pedersen(ddh, proof, *extras)
        assert check_proof_c1   # TODO: Remove

        ddh, proof = self._extract_ddh_proof(proof_c2)
        check_proof_c2 = self._verify_chaum_pedersen(ddh, proof, *extras)
        assert check_proof_c2   # TODO: Remove

        return check_proof_c1 and check_proof_c2

    def verify_niddh(self, enc_niddh, issuer_pub):
        niddh = json.loads(self.decrypt(enc_niddh, issuer_pub).decode('utf-8')) # TODO
        niddh = self._deserialize_ddh_proof(niddh)
        ddh, proof = self._extract_ddh_proof(niddh)
        extras = (issuer_pub['ecc'],)                           # TODO
        return self._verify_chaum_pedersen(ddh, proof, *extras)


    def publish_ack(self, s_prf, m, c_r, nirenc, enc_decryptor, enc_niddh, issuer_pub):
    
        # VERIFIER etrieves decryptor created for them by ISSUER
        decryptor = self.retrieve_decryptor(issuer_pub, enc_decryptor)
    
        # VERIFIER decrypts the re-encrypted commitment
        dec_m = self.decrypt_commitment(c_r, decryptor)
    
        # VERIFIER checks content of document
        check_m_integrity = self.check_message_integrity(m, dec_m)
        assert check_m_integrity    # TODO: Remove
    
        # VERIFIER verifies NIRENC proof
        check_nirenc = self.verify_nirenc(nirenc, issuer_pub)
        assert check_nirenc         # TODO: Remove
    
        # VERIFIER verifies NIDDH proof
        check_niddh = self.verify_niddh(enc_niddh, issuer_pub)
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
