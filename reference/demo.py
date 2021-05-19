import json
from protocol import KeyGenerator, Holder, Issuer, Verifier

if __name__ == '__main__':

    CURVE = 'P-384'             # Cryptosystem config

    kg = KeyGenerator(CURVE)
    holder_key   = kg.generate_keys(CURVE)
    issuer_key   = kg.generate_keys(CURVE)
    verifier_key = kg.generate_keys(CURVE)

    # Setup involved parties
    holder = Holder(CURVE)
    issuer = Issuer(CURVE)
    verifier = Verifier(CURVE)

    # Involved parties publish their keys
    holder_pub = holder.get_public_shares()
    issuer_pub = issuer.get_public_shares()
    verifier_pub = verifier.get_public_shares()

    # The document under verification
    t = "This is a message to be encrypted".encode('utf-8')

    print('\nstep 1')                           # step 1

    # ISSUER commits to document t
    s_awd, c, r = issuer.publish_award(t)

    # ISSUER stores r privately, publishes the commitment c and
    # publishes s_awd (ledger) sending it also to HOLDER
    print('s_awd:', s_awd)
    print('c:', c)
    print('r:', r)

    print('\nstep 2')                           # step 2

    # HOLDER makes a request for proof of t (on behalf of ISSUER)
    # addressed to VERIFIER
    s_req = holder.publish_request(s_awd, verifier_pub)

    # HOLDER publishes s_req (ledger)
    print('s_req:', s_req)

    print('\nstep 3')                           # step 3

    # ISSUER generates the requested proof for VERIFIER, using commitment c
    # to the original document and the privately stored randomness r used
    # to generate it
    s_prf, proof = issuer.publish_proof(s_req, r, c, verifier_pub)

    # ISSUER publishes s_prf (ledger) and sends proof to VERIFIER
    print('s_prf:', s_prf)
    print('proof:', json.dumps(proof, indent=2))

    print('\nstep 4')                           # step 4

    # VERIFIER verifies proof against document and ISSUER's key
    s_ack, result = verifier.publish_ack(s_prf, t, proof, issuer_pub)

    # VERIFIER publishes s_ack (ledger) and the verification result
    print('s_ack:', s_ack)
    print('[%s] Verification: %s' % (('+', 'SUCCESS') if result else ('-',
        'FAILURE')))
