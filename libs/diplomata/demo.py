import json
from diplomata.protocol import KeyManager, Holder, Issuer, Verifier

if __name__ == '__main__':

    CURVE = 'P-384'             # Cryptosystem config

    km = KeyManager(CURVE)
    holder_key   = km.generate_keys(serialized=True)
    issuer_key   = km.generate_keys(serialized=True)
    verifier_key = km.generate_keys(serialized=True)


    # Setup involved parties
    holder   = Holder.create_from_key(curve=CURVE, key=holder_key)
    issuer   = Issuer.create_from_key(curve=CURVE, key=issuer_key)
    verifier = Verifier.create_from_key(curve=CURVE, key=verifier_key)


    # Involved parties publish their keys
    holder_pub   = holder.get_public_shares()
    issuer_pub   = issuer.get_public_shares()
    verifier_pub = verifier.get_public_shares()


    # The document under verification
    title = "This is a qualification"


    print('\nstep 1')                           # step 1

    # ISSUER commits to document t
    s_awd, c, r = issuer.publish_award(title)

    # ISSUER stores r privately, publishes the commitment c and
    # publishes s_awd (ledger) sending it also to HOLDER
    print('s_awd:', s_awd)
    print('c:', c)
    print('r:', r)


    print('\nstep 2')                           # step 2

    # HOLDER makes a request for proof of t (on behalf of ISSUER)
    # addressed to VERIFIER

    # TODO
    from diplomata.protocol import AWARD
    payload = holder.create_tag(AWARD, c=c)
    assert holder.verify_signature(s_awd, issuer_pub, payload)

    s_req = holder.publish_request(s_awd, verifier_pub)

    print('s_req:', s_req)


    print('\nstep 3')                           # step 3

    # ISSUER generates the requested proof for VERIFIER, using commitment c
    # to the original document and the privately stored randomness r used
    # to generate it

    # TODO
    from diplomata.protocol import REQUEST
    payload = issuer.create_tag(REQUEST, s_awd=s_awd, verifier=verifier_pub)
    assert issuer.verify_signature(s_req, holder_pub, payload)

    s_prf, proof = issuer.publish_proof(s_req, r, c, verifier_pub)

    # ISSUER publishes s_prf (ledger) and sends proof to VERIFIER
    print('s_prf:', s_prf)
    print('proof:', json.dumps(proof, indent=2))


    print('\nstep 4')                           # step 4

    # VERIFIER verifies proof against document and ISSUER's key

    # TODO
    from diplomata.protocol import PROOF
    payload = verifier.create_tag(PROOF, s_req=s_req, **proof)
    assert verifier.verify_signature(s_prf, issuer_pub, payload)

    s_ack, result = verifier.publish_ack(s_prf, title, proof, issuer_pub)

    # VERIFIER publishes s_ack (ledger) and the verification result
    print('s_ack:', s_ack)
    print('[%s] Verification: %s' % (('+', 'SUCCESS') if result else ('-',
        'FAILURE')))
