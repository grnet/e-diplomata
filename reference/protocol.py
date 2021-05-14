from util import *


class Party(object):

    def __init__(self, curve):
        self.curve = curve
        self.key = self._keygen(self.curve)
        self.signer = DSS.new(self.key['ecc'], 'fips-186-3')

    @staticmethod
    def _keygen(curve):
        return {
            'ecc': ECC.generate(curve=curve.desc),
            'nacl': PrivateKey.generate(),
        }

    def get_public_shares(self):
        return {
            'ecc': self.key['ecc'].pointQ,
            'nacl': self.key['nacl'].public_key,
        }

    def sign(self, payload):
        hc = SHA384.new(payload)
        signature = self.signer.sign(hc)
        return signature

    def verify_signature(self, s):
        pass

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

    # TODO: Remove it when chaum-pedersen infra is ready
    def auxiliary_chaum_pedersen_proof(self, u, w):
        pub = ecc_pub_key(self.key['ecc'])    # public; TODO
        v = pub
        z = int(self.key['ecc'].d)              # secret; TODO
        extras = (pub,)
        proof = chaum_pedersen(self.curve, (u, v, w), z, *extras)
        return proof

    def set_nirenc(self, proof_c1, proof_c2):
        return {
            'proof_c1': proof_c1,
            'proof_c2': proof_c2,
        }

    def extract_nirenc(self, nirenc):
        proof_c1 = nirenc['proof_c1']
        proof_c2 = nirenc['proof_c2']
        return proof_c1, proof_c2


class Holder(Party):

    def __init__(self, curve):
        super().__init__(curve)

    def publish_request(self, s_awd, verifier_pub):
        pub = verifier_pub['ecc']
        payload = (f'REQUEST s_awd={s_awd} ver_pub={pub}').encode('utf-8')
        s_req = self.sign(payload)
        return s_req


class Issuer(Party):

    def __init__(self, curve):
        super().__init__(curve)

    def commit_to_document(self, document):
        return commit(self.curve, ecc_pub_key(self.key['ecc']), document)

    def publish_award(self, t):
        c, r = self.commit_to_document(t)   # c1, c2

        c1, c2 = extract_cipher(c)
        payload = f'AWARD c1={c1.xy} c2={c2.xy}'.encode('utf-8')

        s_awd = self.sign(payload)
        return s_awd, c, r

    def reencrypt_commitment(self, c):
        """
        """
        # TODO: Simplify conversions
        c_r, r_r = elgamal_reencrypt(
            self.curve,
            ecc_pub_key(self.key['ecc']),
            c,
        )
        return c_r, r_r

    def create_decryptor(self, r1, r2, verifier_pub):
        r_tilde = r1 + r2
        decryptor = ecc_pub_key(self.key['ecc']) * r_tilde              # TODO

        enc_decryptor = self.encrypt(
            str(decryptor.xy).encode('utf-8'),
            verifier_pub
        )

        return decryptor, enc_decryptor

    def generate_nirenc(self, c, c_r, verifier_pub):
        c1  , c2   = extract_cipher(c)
        c1_r, c2_r = extract_cipher(c_r)

        # TODO:
        pub = ecc_pub_key(self.key['ecc'])
        proof_c1 = set_ddh_proof(
            (c1, pub, c1_r),
            self.auxiliary_chaum_pedersen_proof(c1, c1_r)   # TODO: Remove
        )
        proof_c2 = set_ddh_proof(
            (c2, pub, c2_r),
            self.auxiliary_chaum_pedersen_proof(c2, c2_r)   # TODO: Remove
        )

        nirenc = self.set_nirenc(proof_c1, proof_c2)
        return nirenc

    def serialize_nirenc(self, nirenc):
        proof_c1, proof_c2 = self.extract_nirenc(nirenc)
        return {
            'proof_c1': serialize_ddh_proof(proof_c1),
            'proof_c2': serialize_ddh_proof(proof_c2),
        }

    def generate_niddh(self, r1, r2, verifier_pub):
        # TODO
        g = self.curve.G
        g_r = g * r1
        g_r_r = g * r2
        pub = ecc_pub_key(self.key['ecc'])    # public; TODO
        niddh = set_ddh_proof(
            (g_r, pub, g_r_r),
            self.auxiliary_chaum_pedersen_proof(g_r, g_r_r)
        )
        niddh = serialize_ddh_proof(niddh)

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
        nirenc = self.serialize_nirenc(nirenc)

        # Create and encrypt NIDDH of the above decryptor addressed to VERIFIER
        niddh, enc_niddh = self.generate_niddh(r, r_r, verifier_pub)

        # Create PROOF tag
        nirenc_str = json.dumps(nirenc)
        c_r_1, c_r_2 = extract_cipher(c_r)
        payload = (f'PROOF s_req={s_req} c_r=({c_r_1.xy, c_r_2.xy}) '
                   f'{nirenc_str} {enc_decryptor} '
                   f'{enc_niddh}'.encode('utf-8'))
        s_prf = self.sign(payload)

        return (s_prf, c_r, nirenc, enc_decryptor, enc_niddh)


class Verifier(Party):

    def __init__(self, curve):
        super().__init__(curve)

    def retrieve_decryptor(self, issuer_pub, enc_decryptor):
        dec_decryptor = self.decrypt(enc_decryptor, issuer_pub).decode('utf-8')

        extract_coords = re.match(r'^\D*(\d+)\D+(\d+)\D*$', dec_decryptor)
        x_affine = int(extract_coords.group(1))
        y_affine = int(extract_coords.group(2))
        # TODO: Raise exception for caller?
        if not extract_coords:
            payload = f'FAIL {s_prf}'.encode('utf-8')
            s_ack = verifier.sign(payload)
            return s_ack
        decryptor = ECC.EccPoint(x_affine, y_affine, curve=self.curve.desc)
        return decryptor

    def decrypt_commitment(self, c_r, decryptor):
        dec_m = elgamal_drenc(c_r, decryptor)
        return dec_m

    def check_message_integrity(self, message, dec_m):
        """
        Checks that dec_m coincides with the hash of message,
        seen as ECC points
        """
        g = self.curve.G
        h = hash_into_integer(message)
        h_ecc_point = g * h
        return dec_m == h_ecc_point

    def deserialize_nirenc(self, nirenc):
        proof_c1, proof_c2 = self.extract_nirenc(nirenc)
        return {
            'proof_c1': deserialize_ddh_proof(self.curve, proof_c1),
            'proof_c2': deserialize_ddh_proof(self.curve, proof_c2),
        }

    def verify_nirenc(self, nirenc, issuer_pub):

        nirenc = self.deserialize_nirenc(nirenc)
        proof_c1, proof_c2 = self.extract_nirenc(nirenc)
        extras = (issuer_pub['ecc'],)

        ddh, proof = extract_ddh_proof(proof_c1)
        check_proof_c1 = chaum_pedersen_verify(self.curve, ddh, proof, *extras)
        assert check_proof_c1   # TODO: Remove

        ddh, proof = extract_ddh_proof(proof_c2)
        check_proof_c2 = chaum_pedersen_verify(self.curve, ddh, proof, *extras)
        assert check_proof_c2   # TODO: Remove

        return check_proof_c1 and check_proof_c2

    def verify_niddh(self, enc_niddh, issuer_pub):
        niddh = json.loads(self.decrypt(enc_niddh, issuer_pub).decode('utf-8')) # TODO
        niddh = deserialize_ddh_proof(self.curve, niddh)
        ddh, proof = extract_ddh_proof(niddh)
        extras = (issuer_pub['ecc'],)
        return chaum_pedersen_verify(self.curve, ddh, proof, *extras)   # TODO


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
