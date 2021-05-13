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

    def generate_chaum_pedersen_proof(self, a, b):
        return chaum_pedersen(self.curve, self.key['ecc'], a, b)

    def verify_chaum_pedersen_proof(self, public, a, b, u, v, s, d):
        return chaum_pedersen_verify(
            self.curve,
            public['ecc'],
            a, b, u, v, s, d
        )


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
        # order = self.curve.order       # Maybe use in payload?
        commitment, r = self.commit_to_document(t)
        c1, c2 = extract_cipher(commitment)                         # TODO
        payload = f'AWARD c1={c1.xy} c2={c2.xy}'.encode('utf-8')
        s_awd = self.sign(payload)
        commitment = (c1, c2)
        return s_awd, commitment, r

    def reencrypt_commitment(self, commitment):
        """
        input: (c1, c2)
        outout: (c1_r, c2_r), r_r
        """
        # TODO: Simplify conversions
        cipher_r, r_r = reencrypt(
            self.curve,
            ecc_pub_key(self.key['ecc']),
            set_cipher(*commitment),
        )
        c1_r, c2_r = extract_cipher(cipher_r)
        return (c1_r, c2_r), r_r

    def create_decryptor(self, r1, r2, verifier_pub):
        r_tilde = r1 + r2
        decryptor = ecc_pub_key(self.key['ecc']) * r_tilde              # TODO

        enc_decryptor = self.encrypt(
            str(decryptor.xy).encode('utf-8'),
            verifier_pub
        )

        return decryptor, enc_decryptor

    def generate_nirenc(self, c, c_r, verifier_pub):
        c1, c2 = c
        c1_r, c2_r = c_r
        proof_c1 = c1, c1_r, *self.generate_chaum_pedersen_proof(c1, c1_r)
        proof_c2 = c2, c2_r, *self.generate_chaum_pedersen_proof(c2, c2_r)

        nirenc = {
            'proof_c1': proof_c1,
            'proof_c2': proof_c2,
        }
        return nirenc


    def generate_niddh(self, r1, r2, verifier_pub):
        # TODO
        g = self.curve.G
        g_r = g * r1
        g_r_r = g * r2
        u, v, s, d = self.generate_chaum_pedersen_proof(g_r, g_r_r)
        niddh = serialize_chaum_pedersen(g_r, g_r_r, u, v, s, d)

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

        # Create and encrypt NIDDH of the above decryptor addressed to VERIFIER
        niddh, enc_niddh = self.generate_niddh(r, r_r, verifier_pub)

        # Create PROOF tag
        # TODO: Define and use serialize_nirenc
        nirenc_str = json.dumps({
            'proof_c1': serialize_chaum_pedersen(*nirenc['proof_c1']),
            'proof_c2': serialize_chaum_pedersen(*nirenc['proof_c2']),
        })
        payload = (f'PROOF s_req={s_req} c_r=({c_r[0].xy, c_r[1].xy}) '
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
        # TODO
        c1, c2 = c_r
        cipher_r = set_cipher(c1, c2)
        dec_m = drenc(cipher_r, decryptor)
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
    # proof_c1, proof_c2 = nirenc
    proof_c1 = nirenc['proof_c1']
    proof_c2 = nirenc['proof_c2']

    a, b, u, v, s, d = proof_c1
    check_proof_c1 = verifier.verify_chaum_pedersen_proof(issuer_pub, a, b, u, v, s, d)
    assert check_proof_c1
    if not check_proof_c1:
        payload = f'FAIL {s_prf}'.encode('utf-8')
        s_ack = verifier.sign(payload)
        return s_ack

    a, b, u, v, s, d = proof_c2
    check_proof_c2 = verifier.verify_chaum_pedersen_proof(issuer_pub, a, b, u, v, s, d)
    assert check_proof_c2
    if not check_proof_c2:
        payload = f'FAIL {s_prf}'.encode('utf-8')
        s_ack = verifier.sign(payload)
        return s_ack

    # Verify NIDDH proof
    dec_niddh = verifier.decrypt(enc_niddh, issuer_pub)
    a, b, u, v, s, d = deserialize_chaum_pedersen(curve, json.loads(dec_niddh))
    check_proof_r_r = verifier.verify_chaum_pedersen_proof(issuer_pub, a, b, u, v, s, d)
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
    print('c1:', c[0].xy, 'c2:', c[1].xy, 's_awd:', s_awd, 'r:', r)

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
