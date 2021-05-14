from lib import *


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
        decryptor = ECC.EccPoint(x_affine, y_affine, curve=curve.desc)
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


def step_four(issuer_pub, verifier, c_r, nirenc,
              enc_decryptor, enc_niddh, m):

    # VERIFIER etrieves decryptor created for them by ISSUER
    decryptor = verifier.retrieve_decryptor(issuer_pub, enc_decryptor)

    # VERIFIER decrypts the re-encrypted commitment
    dec_m = verifier.decrypt_commitment(c_r, decryptor)

    # VERIFIER checks content of document
    check_m_integrity = verifier.check_message_integrity(m, dec_m)
    assert check_m_integrity
    if not check_m_integrity:
        payload = f'NACK {s_prf}'.encode('utf-8')
        s_ack = verifier.sign(payload)
        return s_ack

    # Verify NIRENC proof
    nirenc = verifier.deserialize_nirenc(nirenc)
    proof_c1, proof_c2 = verifier.extract_nirenc(nirenc)
    extras = (issuer_pub['ecc'],)

    ddh, proof = extract_ddh_proof(proof_c1)
    check_proof_c1 = chaum_pedersen_verify(curve, ddh, proof, *extras)
    assert check_proof_c1
    if not check_proof_c1:
        payload = f'FAIL {s_prf}'.encode('utf-8')
        s_ack = verifier.sign(payload)
        return s_ack

    ddh, proof = extract_ddh_proof(proof_c2)
    check_proof_c2 = chaum_pedersen_verify(curve, ddh, proof, *extras)
    assert check_proof_c2
    if not check_proof_c2:
        payload = f'FAIL {s_prf}'.encode('utf-8')
        s_ack = verifier.sign(payload)
        return s_ack

    # Verify NIDDH proof
    niddh = json.loads(verifier.decrypt(enc_niddh, issuer_pub).decode('utf-8'))
    niddh = deserialize_ddh_proof(curve, niddh)
    ddh, proof = extract_ddh_proof(niddh)
    extras = (issuer_pub['ecc'],)
    check_proof_r_r = chaum_pedersen_verify(curve, ddh, proof, *extras)
    assert check_proof_r_r
    if not check_proof_r_r:
        payload = f'FAIL {s_prf}'.encode('utf-8')
        s_ack = verifier.sign(payload)
        return s_ack

    # All checks succeded, acknowledge proof
    payload = f'ACK {s_prf}'.encode('utf-8')
    s_ack = verifier.sign(payload)
    return s_ack


if __name__ == '__main__':

    curve = gen_curve('P-384')

    # Setup involved parties
    holder = Holder(curve)
    issuer = Issuer(curve)
    verifier = Verifier(curve)

    # Invloved parties publish their keys
    holder_pub = holder.get_public_shares()
    issuer_pub = issuer.get_public_shares()
    verifier_pub = verifier.get_public_shares()

    m = "This is a message to be encrypted".encode('utf-8')

    print()
    print('step 1')
    s_awd, c, r = issuer.publish_award(m)
    # ISSUER stores privately r used for encryption and sends s_awd to the HOLDER
    c1, c2 = extract_cipher(c)
    print('c1:', c1.xy, 'c2:', c2.xy, 's_awd:', s_awd, 'r:', r)

    print()
    print('step 2')
    s_req = holder.publish_request(s_awd, verifier_pub)
    # The request signature can be verified by the ISSUER in order to identify
    # the HOLDER and ensure that this is the true holder of the qualification
    # committed to at s_awd
    print('s_req:', s_req)

    print()
    print('step 3')
    s_prf, c_r, nirenc, enc_decryptor, enc_niddh = issuer.publish_proof(
        r, c, s_req, verifier_pub)
    print('s_prf:', s_prf)

    print()
    print('step 4')
    s_ack = step_four(issuer_pub, verifier, c_r, nirenc,
                      enc_decryptor, enc_niddh, m)
    print('s_ack:', s_ack)
