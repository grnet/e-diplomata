from diplomata.protocol import *
from diplomata.util import *
import pytest

def test_transaction_logic_layer():

    # Setup involved parties

    holder = Holder()
    issuer = Issuer()
    verifier = Verifier()

    holder_pub = holder.get_public(serialized=False)
    issuer_pub = issuer.get_public(serialized=False)
    ver_pub = verifier.get_public(serialized=False)

    auditor = Party()

    # Run protocol

    title = b'This is a qualification'

    # step 1
    c, r = issuer.commit_to_document(title)
    tag = issuer.create_tag(AWARD,c=issuer.serialize_cipher(c))
    s_awd = issuer.sign(tag, serialized=False)

    # audit
    tag = auditor.create_tag(AWARD, c=auditor.serialize_cipher(c))
    audit = auditor.verify_signature(s_awd, issuer_pub, tag, 
        from_serialized=False)
    assert audit

    # step 2
    tag = holder.create_tag(REQUEST, 
        verifier=ver_pub,
        s_awd=s_awd 
    )
    s_req = holder.sign(tag, serialized=False)

    # audit
    tag = auditor.create_tag(REQUEST, verifier=ver_pub, s_awd=s_awd)
    audit = auditor.verify_signature(s_req, holder_pub, tag, 
        from_serialized=False)
    assert audit

    # step 3
    proof = issuer.generate_proof(c, r)
    tag = issuer.create_tag(PROOF, s_req=s_req, **proof)
    s_prf = issuer.sign(tag, serialized=False)

    # audit
    tag = auditor.create_tag(PROOF, s_req=s_req, **proof)
    audit = auditor.verify_signature(s_prf, issuer_pub, tag, 
        from_serialized=False)
    assert audit

    # step 4
    result = verifier.verify_proof(proof, title, issuer_pub)
    tag = verifier.create_tag(
        ACK if result else NACK,
        result=result,
        s_prf=s_prf)
    s_ack = verifier.sign(tag, serialized=False)

    assert result

    # audit
    tag = auditor.create_tag(ACK, result=result, s_prf=s_prf)
    audit = auditor.verify_signature(s_ack, ver_pub, tag,
        from_serialized=False)
    assert audit


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
def test_presentation_layer(config):

    # Setup

    km = KeyManager(**config)

    # Create and publish keys

    holder_key = km.generate_keys()
    holder_pub = km.get_public_shares(holder_key)

    issuer_key = km.generate_keys()
    issuer_pub = km.get_public_shares(issuer_key)

    verifier_key = km.generate_keys()
    ver_pub = km.get_public_shares(verifier_key)

    # Load involved parties from keys

    holder = Holder.from_key(key=holder_key, **config)
    issuer = Issuer.from_key(key=issuer_key, **config)
    verifier = Verifier.from_key(key=verifier_key, **config)

    # Check public coumterparts

    assert holder_pub == holder.get_public()
    assert issuer_pub == issuer.get_public()
    assert ver_pub == verifier.get_public()

    # Check alternative setup

    assert holder_pub == Holder(key=holder_key, **config).get_public()
    assert issuer_pub == Issuer(key=issuer_key, **config).get_public()
    assert ver_pub == Verifier(key=verifier_key, **config).get_public()

    # Run protocol

    title = 'This is a qualification'

    # step 1, TODO: Remove signature verification
    s_awd, c, r = issuer.publish_award(title)

    # step 2, TODO: Remove signature verification
    from diplomata.protocol import AWARD
    tag = holder.create_tag(AWARD, c=c)
    _issuer_pub = holder._key_manager._unflatten_public(issuer_pub)
    assert holder.verify_signature(s_awd, _issuer_pub, tag)
    s_req = holder.publish_request(s_awd, ver_pub)

    # step 3, TODO: Remove signature verification
    from diplomata.protocol import REQUEST
    tag = issuer.create_tag(REQUEST, s_awd=s_awd, verifier=ver_pub)
    _holder_pub = issuer._key_manager._unflatten_public(holder_pub)
    assert issuer.verify_signature(s_req, _holder_pub, tag)
    s_prf, proof = issuer.publish_proof(s_req, r, c, ver_pub)

    # step 4, TODO: Remove signature verification
    from diplomata.protocol import PROOF
    tag = verifier.create_tag(PROOF, s_req=s_req, **proof)
    _issuer_pub = verifier._key_manager._unflatten_public(issuer_pub)
    assert verifier.verify_signature(s_prf, _issuer_pub, tag)
    s_ack, result = verifier.publish_ack(s_prf, title, proof, issuer_pub)

    assert result
