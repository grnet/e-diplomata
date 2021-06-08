"""
Diplomata Demo Script
"""

import sys
import argparse
import json
from diplomata.protocol import KeyManager, Holder, Issuer, Verifier

def _json_dump(payload):
    print(json.dumps(payload, indent=2))

if __name__ == '__main__':
    prog = sys.argv[0]
    parser = argparse.ArgumentParser(**{
        'prog': prog,
        'usage': 'python3 %s [OPTIONS]' % prog,
        'epilog': '\n',
        'description': __doc__,
        'epilog': '',
    })

    parser.add_argument('--curve', type=str, default='P-384', 
            help="Elliptic curve of El-Gamal cryptosystem (default: P-384)")
    parser.add_argument('--title', type=str, default='This is a qualification', 
            help="Content of title under verification (default: \"This is\
            a qualification\")")
    parser.add_argument('--hexify', action='store_true', default=False,
            help="Hexify big integers at serialization (default: False)")
    parser.add_argument('--flatten', action='store_true', default=False,
            help="Flatten serialized objects (default: False)")
    parser.add_argument('--verbose', action='store_true', default=False,
            help="Display computation results at each step (default: False)")

    args = parser.parse_args()

    curve = args.curve
    title = args.title
    hexify = args.hexify
    flatten = args.flatten
    verbose = args.verbose


    # Setup

    config = {
        'curve': args.curve,
        'hexifier': args.hexify,
        'flattener': args.flatten,
    }

    km = KeyManager(**config)

    holder_key = km.generate_keys()
    issuer_key = km.generate_keys()
    verifier_key = km.generate_keys()

    holder = Holder.from_key(holder_key, **config)
    issuer = Issuer.from_key(issuer_key, **config)
    verifier = Verifier.from_key(verifier_key, **config)

    holder_pub = holder.get_public()
    issuer_pub = issuer.get_public()
    verifier_pub = verifier.get_public()


    # Run protocol

    if verbose:
        print('\nstep 1')                           # step 1
    s_awd, c, r = issuer.publish_award(title)
    if verbose:
        _json_dump({
            's_awd': s_awd,
            'c': c,
            'r': r,
        })


    if verbose:
        print('\nstep 2')                           # step 2
    # TODO
    from diplomata.protocol import AWARD
    tag = holder.create_tag(AWARD, c=c)
    _issuer_pub = holder._key_manager._unflatten_public(issuer_pub)
    assert holder.verify_signature(s_awd, _issuer_pub, tag)
    s_req = holder.publish_request(s_awd, verifier_pub)
    if verbose:
        _json_dump({
            's_req': s_req,
        })


    if verbose:
        print('\nstep 3')                           # step 3
    # TODO
    from diplomata.protocol import REQUEST
    tag = issuer.create_tag(REQUEST, s_awd=s_awd, verifier=verifier_pub)
    _holder_pub = issuer._key_manager._unflatten_public(holder_pub)
    assert issuer.verify_signature(s_req, _holder_pub, tag)
    s_prf, proof = issuer.publish_proof(s_req, r, c, verifier_pub)
    if verbose:
        _json_dump({
            's_prf': s_prf,
            'proof': proof,
        })


    if verbose:
        print('\nstep 4')                           # step 4
    # TODO
    from diplomata.protocol import PROOF
    tag = verifier.create_tag(PROOF, s_req=s_req, **proof)
    _issuer_pub = verifier._key_manager._unflatten_public(issuer_pub)
    assert verifier.verify_signature(s_prf, _issuer_pub, tag)
    s_ack, result = verifier.publish_ack(s_prf, title, proof, issuer_pub)
    if verbose:
        _json_dump({
            's_ack': s_ack,
        })

    print('[%s] Verification: %s' % (('+', 'SUCCESS') if result else ('-',
        'FAILURE')))
