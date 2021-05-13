from lib import *


class Party(object):

    def __init__(self, curve):
        self.curve = curve
        self.key = keygen(self.curve)

    def sign(self, payload):
        signer = DSS.new(self.key['ecc'], 'fips-186-3')
        hc = SHA384.new(payload)
        signature = signer.sign(hc)
        return signature

    def generate_chaum_pedersen_proof(self, a, b):
        return chaum_pedersen(self.curve, self.key['ecc'], a, b)

    def verify_chaum_pedersen_proof(self, issuer, a, b, u, v, s, d):
        return chaum_pedersen_verify(
            self.curve,
            ecc_pub_key(issuer.key['ecc']),
            a, b, u, v, s, d
        )


class Holder(Party):

    def __init__(self, curve):
        super().__init__(curve)

    def publish_request(self, verifier, s_awd):
        ver_pub = ecc_pub_key(verifier.key['ecc'])  # TODO
        payload = (f'REQUEST s_awd={s_awd} ver_pub={ver_pub}').encode('utf-8')
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
        outout: (c1_r, c2_r)
        """
        # TODO: Simplify conversions
        cipher_r, r_r = reencrypt(
            self.curve,
            ecc_pub_key(self.key['ecc']),
            set_cipher(*commitment),
        )
        c1_r, c2_r = extract_cipher(cipher_r)
        return (c1_r, c2_r), r_r

    def create_decryptor(self, r1, r2, verifier):
        box = Box(self.key['nacl'], verifier.key['nacl'].public_key)
        r_tilde = r1 + r2
        decryptor = ecc_pub_key(self.key['ecc']) * r_tilde              # TODO
        enc_decryptor = box.encrypt(str(decryptor.xy).encode('utf-8'))  # TODO
        return decryptor, enc_decryptor

    def generate_nirenc(self, c, c_r):
        # TODO
        c1, c2 = c
        c1_r, c2_r = c_r
        proof_c1 = c1, c1_r, *self.generate_chaum_pedersen_proof(c1, c1_r)
        proof_c2 = c2, c2_r, *self.generate_chaum_pedersen_proof(c2, c2_r)
        nirenc = proof_c1, proof_c2

        # TODO
        nirenc_str = json.dumps({
            'proof_c1': serialize_chaum_pedersen(*proof_c1),
            'proof_c2': serialize_chaum_pedersen(*proof_c2),
        })

        # TODO
        box = Box(self.key['nacl'], verifier.key['nacl'].public_key)
        enc_nirenc = box.encrypt(json.dumps(nirenc_str).encode('utf-8'))

        return nirenc, nirenc_str, enc_nirenc


    def generate_niddh(self, r1, r2, verifier):
        # TODO
        g = self.curve.G
        g_r = g * r1
        g_r_r = g * r2
        u, v, s, d = self.generate_chaum_pedersen_proof(g_r, g_r_r)
        niddh = serialize_chaum_pedersen(g_r, g_r_r, u, v, s, d)

        # TODO
        box = Box(self.key['nacl'], verifier.key['nacl'].public_key)
        enc_niddh = box.encrypt(json.dumps(niddh).encode('utf-8'))

        return niddh, enc_niddh



class Verifier(Party):

    def __init__(self, curve):
        super().__init__(curve)

    def retrieve_decryptor(self, issuer, enc_decryptor):
        box = Box(self.key['nacl'], issuer.key['nacl'].public_key)
        dec_decryptor = box.decrypt(enc_decryptor).decode('utf-8')
        extract_coords = re.match(r'^\D*(\d+)\D+(\d+)\D*$', dec_decryptor)
        x_affine = int(extract_coords.group(1))
        y_affine = int(extract_coords.group(2))
        # TODO
        if not extract_coords:
            payload = f'FAIL {s_prf}'.encode('utf-8')
            s_ack = verifier.sign(payload)
            return s_ack
        decryptor = ECC.EccPoint(x_affine, y_affine, curve=curve.desc)
        return decryptor


def step_three(curve, issuer, r, c, s_req, verifier):

    # re-encrypt commitmentn
    c_r, r_r = issuer.reencrypt_commitment(c)

    # create NIRENC
    nirenc, nirenc_str, enc_nirenc = issuer.generate_nirenc(c, c_r)

    # Create and encrypt decryptor
    decryptor, enc_decryptor = issuer.create_decryptor(r, r_r, verifier)

    # Create and encrypt NIDDH of the above decryptor addressed to VERIFIER
    niddh, enc_niddh = issuer.generate_niddh(r, r_r, verifier)

    payload = (f'PROOF s_req={s_req} c_r=({c_r[0].xy, c_r[1].xy}) '
               f'{nirenc_str} {enc_decryptor} '
               f'{enc_niddh}'.encode('utf-8'))
    s_prf = issuer.sign(payload)

    # TODO: Maybe encrypt nirenc as enc_nirenc before giving it out?

    return (s_prf, c_r, nirenc, enc_decryptor, enc_niddh)

def step_four(curve, issuer, verifier, c_r, nirenc,
              enc_decryptor, enc_niddh, m):

    # Retrieve decryptor created by ISSUER for VERIFIER
    decryptor = verifier.retrieve_decryptor(issuer, enc_decryptor)

    # decrypt the re-encryption using the decryptor
    c1, c2 = c_r
    cipher_r = set_cipher(c1, c2)
    dec_m = drenc(cipher_r, decryptor)
    # check that the decrypted hash is the same with the hash of the original
    # document, as an ECC point
    h = hash_into_integer(m)
    g = curve.G
    h_ecc_point = g * h
    if dec_m != h_ecc_point:
        payload = f'NACK {s_prf}'.encode('utf-8')
        s_ack = verifier.sign(payload)
        return s_ack
    # check the NIRENC proof
    proof_c1, proof_c2 = nirenc
    a, b, u, v, s, d = proof_c1
    check_proof_c1 = verifier.verify_chaum_pedersen_proof(issuer, a, b, u, v, s, d)
    assert check_proof_c1
    if not check_proof_c1:
        payload = f'FAIL {s_prf}'.encode('utf-8')
        s_ack = verifier.sign(payload)
        return s_ack
    a, b, u, v, s, d = proof_c2
    check_proof_c2 = verifier.verify_chaum_pedersen_proof(issuer, a, b, u, v, s, d)
    assert check_proof_c2
    if not check_proof_c2:
        payload = f'FAIL {s_prf}'.encode('utf-8')
        s_ack = verifier.sign(payload)
        return s_ack
    # check the NIDDH proof
    # TODO: Transfer box inside verifier methods using it
    verifier_box = Box(verifier.key['nacl'], issuer.key['nacl'].public_key)
    dec_niddh = verifier_box.decrypt(enc_niddh)
    check_proof_r_r = verifier.verify_chaum_pedersen_proof(issuer, a, b, u, v, s, d)
    assert check_proof_r_r
    if not check_proof_r_r:
        payload = f'FAIL {s_prf}'.encode('utf-8')
        s_ack = verifier.sign(payload)
        return s_ack
    payload = f'ACK {s_prf}'.encode('utf-8')
    s_ack = verifier.sign(payload)
    return s_ack


if __name__ == '__main__':

    curve = gen_curve('P-384')

    # Setup key-owning entities

    holder = Holder(curve)
    issuer = Issuer(curve)
    verifier = Verifier(curve)

    m = "This is a message to be encrypted".encode('utf-8')

    print('step 1')
    s_awd, c, r = issuer.publish_award(m)
    # ISSUER stores privately r used for encryption and sends s_awd to the HOLDER
    print('c1:', c[0].xy, 'c2:', c[1].xy, 's_awd:', s_awd, 'r:', r)
    print()

    print('step_two')
    s_req  = holder.publish_request(verifier, s_awd)
    # The request signature can be verified by the ISSUER in order to identify
    # the HOLDER and ensure that this is the true holder of the qualification
    # committed to at s_awd
    print('s_req:', s_req)
    print('step_three')
    s_prf, c_r, nirenc, enc_decryptor, enc_niddh = step_three(
        curve, issuer, r, c, s_req, verifier)
    print('s_prf:', s_prf)
    print('step_four')
    s_ack = step_four(curve, issuer, verifier, c_r, nirenc,
                      enc_decryptor, enc_niddh, m)
    print('s_ack:', s_ack)
