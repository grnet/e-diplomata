from diplomata.protocol import *
from diplomata.util import *
import pytest

configs = \
[
    {
        'curve': 'P-384',
        'hexifier': False,
        'flattener': False,
    },
    {
        'curve': 'P-384',
        'hexifier': True,
        'flattener': False,
    },
    {
        'curve': 'P-384',
        'hexifier': False,
        'flattener': True,
    },
    {
        'curve': 'P-384',
        'hexifier': True,
        'flattener': True,
    },
]

@pytest.mark.parametrize('config', configs)
def test_signature(config):
    s = Party(**config)            # signer
    v = Party(**config)            # verifier
    m = b"This is a message"
    sig = s.sign(m)

    pub = s.get_public()
    pub = v._key_manager._unflatten_public(pub)                # TODO

    # success
    verified = v.verify_signature(sig, pub, m)
    assert verified

    # corrupt signature
    corrupt_sig = sig + "00"
    verified = v.verify_signature(corrupt_sig, pub, m)
    assert not verified

    # wrong key
    wrong_pub = Party(**config).get_public()
    wrong_pub = v._key_manager._unflatten_public(wrong_pub)    # TODO
    verified = v.verify_signature(sig, wrong_pub, m)
    assert not verified

    # tamper message
    corrupt_m = m + b"\x00"
    verified = v.verify_signature(sig, pub, corrupt_m)
    assert not verified


@pytest.mark.parametrize('config', configs)
def test_flow(config):

    title = 'This is a qualification'

    # Setup involved parties

    # # Alternative setup
    # holder = Holder(**config)
    # issuer = Issuer(**config)
    # verifier = Verifier(**config)

    # holder_pub = holder.get_public()
    # issuer_pub = issuer.get_public()
    # verifier_pub = verifier.get_public()

    km = KeyManager(**config)

    holder_key = km.generate_keys()
    issuer_key = km.generate_keys()
    verifier_key = km.generate_keys()

    holder = Holder.from_key(key=holder_key, **config)
    issuer = Issuer.from_key(key=issuer_key, **config)
    verifier = Verifier.from_key(key=verifier_key, **config)

    holder_pub = km.get_public_shares(holder_key)
    issuer_pub = km.get_public_shares(issuer_key)
    verifier_pub = km.get_public_shares(verifier_key)

    # import pdb; pdb.set_trace()
    assert holder_pub == holder.get_public()
    assert issuer_pub == issuer.get_public()
    assert verifier_pub == verifier.get_public()

    # Run protocol

    # step 1, TODO: Remove signature verification
    s_awd, c, r = issuer.publish_award(title)

    # step 2, TODO: Remove signature verification
    from diplomata.protocol import AWARD
    payload = holder.create_tag(AWARD, c=c)
    _issuer_pub = holder._key_manager._unflatten_public(issuer_pub)
    assert holder.verify_signature(s_awd, _issuer_pub, payload)
    s_req = holder.publish_request(s_awd, verifier_pub)

    # step 3, TODO: Remove signature verification
    from diplomata.protocol import REQUEST
    payload = issuer.create_tag(REQUEST, s_awd=s_awd, verifier=verifier_pub)
    _holder_pub = issuer._key_manager._unflatten_public(holder_pub)
    assert issuer.verify_signature(s_req, _holder_pub, payload)
    s_prf, proof = issuer.publish_proof(s_req, r, c, verifier_pub)

    # step 4, TODO: Remove signature verification
    from diplomata.protocol import PROOF
    payload = verifier.create_tag(PROOF, s_req=s_req, **proof)
    _issuer_pub = verifier._key_manager._unflatten_public(issuer_pub)
    assert verifier.verify_signature(s_prf, _issuer_pub, payload)
    s_ack, result = verifier.publish_ack(s_prf, title, proof, issuer_pub)

    assert result
