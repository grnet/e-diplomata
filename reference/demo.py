from Cryptodome.Signature import DSS
from structs import *
from util import *
from protocol import *

if __name__ == '__main__':

    CURVE = 'P-384'             # Cryptosystem config

    # Setup involved parties
    holder = Holder(CURVE)
    issuer = Issuer(CURVE)
    verifier = Verifier(CURVE)

    # Involved parties publish their keys
    holder_pub = holder.get_public_shares()
    issuer_pub = issuer.get_public_shares()
    verifier_pub = verifier.get_public_shares()
    import pdb; pdb.set_trace()

    m = "This is a message to be encrypted".encode('utf-8')

    print()
    print('step 1')

    s_awd, c, r = issuer.publish_award(m)   # TODO: Return JSON

    p = Prover(curve='P-384')
    # v = VVerifier(curve='P-384')

    # ISSUER stores privately r used for encryption and sends s_awd to the HOLDER

    c1, c2 = extract_cipher(c)
    print('c1:', c1.xy, 'c2:', c2.xy, 's_awd:', s_awd, 'r:', r)

    print()
    print('step 2')

    s_req = holder.publish_request(s_awd, verifier_pub)     # TODO: Return JSON

    # The request signature can be verified by the ISSUER in order to identify
    # the HOLDER and ensure that this is the true holder of the qualification
    # committed to at s_awd

    print('s_req:', s_req)

    print()
    print('step 3')

    s_prf, c_r, nirenc, enc_decryptor, enc_niddh = issuer.publish_proof(
            r, c, s_req, verifier_pub)  # TODO: Accept/Return JSON

    print('s_prf:', s_prf)

    print()
    print('step 4')

    s_ack = verifier.publish_ack(s_prf, m, c_r, nirenc, enc_decryptor,
            enc_niddh, issuer_pub)      # TODO: Accept JSON

    print('s_ack:', s_ack)
