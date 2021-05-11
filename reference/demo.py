from lib import *        

def step_one(curve, issuer_key, t):
    # order = curve.order       # Maybe use in payload?
    commitment, r = commit(curve, ecc_pub_key(issuer_key), t)
    c1, c2 = extract_cipher(commitment)                         # TODO
    payload = f'AWARD c1={c1.xy} c2={c2.xy}'.encode('utf-8')
    s_awd = sign(issuer_key, payload)
    commitment = (c1, c2)
    return s_awd, commitment, r

def step_two(curve, holder_key, verifier_key, s_awd):
    payload = (f'REQUEST s_awd={s_awd} '
               'ver_pub={ecc_pub_key(verifier_key).xy}').encode('utf-8')
    s_req = sign(holder_key, payload)
    return s_req

def step_three(curve, issuer_key, pub_verifier_key, r, commitment, s_req, issuer_box):
    c1, c2 = c
    pub = ecc_pub_key(issuer_key)
    # re-encrypt c
    cipher = set_cipher(c1, c2)
    cipher_r, r_r = reencrypt(curve, pub, cipher)
    c1_r, c2_r = extract_cipher(cipher_r)
    c_r = (c1_r, c2_r)
    # create NIRENC
    proof_c1 = c1, c1_r, *chaum_pedersen(curve, issuer_key, c1, c1_r)
    proof_c2 = c2, c2_r, *chaum_pedersen(curve, issuer_key, c2, c2_r)
    nirenc = (proof_c1, proof_c2)
    nirenc_str = (serialize_chaum_pedersen(*proof_c1),
                  serialize_chaum_pedersen(*proof_c2))
    # create and encrypt decryptor
    g = curve.G
    r_tilde = r + r_r
    decryptor = pub * r_tilde
    enc_decryptor = issuer_box.encrypt(str(decryptor.xy).encode('utf-8'))
    # create and encrypt NIDDH of decryptor
    g_r = g * r
    g_r_r = g * r_r
    u, v, s, d = chaum_pedersen(curve, issuer_key, g_r, g_r_r)
    niddh = serialize_chaum_pedersen(g_r, g_r_r, u, v, s, d)
    enc_niddh = issuer_box.encrypt(json.dumps(niddh).encode('utf-8'))
    payload = (f'PROOF s_req={s_req} c_r=({c_r[0].xy, c_r[1].xy}) '
               f'{nirenc_str} {enc_decryptor} '
               f'{enc_niddh}'.encode('utf-8'))
    s_prf = sign(issuer_key, payload)
    return (s_prf, c_r, nirenc, enc_decryptor, enc_niddh)

def step_four(curve, issuer_key, verifier_key, c_r, nirenc,
              enc_decryptor, enc_niddh, verifier_box, m):
    # get the decryptor
    dec_decryptor = verifier_box.decrypt(enc_decryptor).decode('utf-8')
    extract_coords = re.match(r'^\D*(\d+)\D+(\d+)\D*$', dec_decryptor)
    x_affine = int(extract_coords.group(1))
    y_affine = int(extract_coords.group(2))
    if not extract_coords:
        payload = f'FAIL {s_prf}'.encode('utf-8')
        s_ack = sign(verifier_key, payload)
        return s_ack
    decryptor = ECC.EccPoint(x_affine, y_affine, curve=curve.desc)
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
        s_ack = sign(verifier_key, payload)
        return s_ack
    # check the NIRENC proof
    proof_c1, proof_c2 = nirenc
    a, b, u, v, s, d = proof_c1
    pub = ecc_pub_key(issuer_key)
    check_proof_c1 = chaum_pedersen_verify(curve, pub, a, b, u, v, s, d)
    if not check_proof_c1:
        payload = f'FAIL {s_prf}'.encode('utf-8')
        s_ack = sign(verifier_key, payload)
        return s_ack
    a, b, u, v, s, d = proof_c2
    check_proof_c2 = chaum_pedersen_verify(curve, pub, a, b, u, v, s, d)
    if not check_proof_c2:
        payload = f'FAIL {s_prf}'.encode('utf-8')
        s_ack = sign(verifier_key, payload)
        return s_ack
    # check the NIDDH proof
    dec_niddh = verifier_box.decrypt(enc_niddh)
    a, b, u, v, s, d = deserialize_chaum_pedersen(curve, json.loads(dec_niddh))
    check_proof_r_r = chaum_pedersen_verify(curve, pub, a, b, u, v, s, d)
    assert(check_proof_r_r)
    if not check_proof_r_r:
        payload = f'FAIL {s_prf}'.encode('utf-8')
        s_ack = sign(verifier_key, payload)
        return s_ack
    payload = f'ACK {s_prf}'.encode('utf-8')
    s_ack = sign(verifier_key, payload)
    return s_ack

if __name__ == '__main__':
    curve = gen_curve('P-384')
    test_encdec(curve)

    # Setup keys

    aux = keygen(curve)
    issuer_key = aux['ecc']
    issuer_nacl_key = aux['nacl']

    aux = keygen(curve)
    holder_key = aux['ecc']
    _ = aux['nacl']

    aux = keygen(curve)
    verifier_key = aux['ecc']
    verifier_nacl_key = aux['nacl']

    #

    m = "This is a message to be encrypted".encode('utf-8')

    issuer_box = Box(issuer_nacl_key, verifier_nacl_key.public_key)
    verifier_box = Box(verifier_nacl_key, issuer_nacl_key.public_key)

    print('step 1')
    s_awd, c, r = step_one(curve, issuer_key, m)
    c1, c2 = c
    print('c1:', c1.xy, 'c2:', c2.xy, 's_awd:', s_awd, 'r:', r)
    print()

    print('step_two')
    s_req  = step_two(curve, holder_key, verifier_key, s_awd)
    print('s_req:', s_req)
    print('step_three')
    s_prf, c_r, nirenc, enc_decryptor, enc_niddh = step_three(
        curve, issuer_key, verifier_key,
        r, (c1, c2), s_req,
        issuer_box)
    print('s_prf:', s_prf)
    print('step_four')
    s_ack = step_four(curve, issuer_key, verifier_key, c_r, nirenc,
                      enc_decryptor, enc_niddh, verifier_box, m)
    print('s_ack:', s_ack)