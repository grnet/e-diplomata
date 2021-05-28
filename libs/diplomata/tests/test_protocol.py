from diplomata.protocol import *
from diplomata.util import *

CURVE = 'P-384'

def test_signature():
    s = Party(CURVE)            # signer
    v = Party(CURVE)            # verifier
    m = b"This is a message"
    sig = s.sign(m)

    pub = s.get_public_shares()

    # success
    verified = v.verify_signature(sig, pub, m)
    assert verified

    # corrupt signature
    corrupt_sig = sig + "00"
    verified = v.verify_signature(corrupt_sig, pub, m)
    assert not verified

    # wrong key
    wrong_pub = Party(CURVE).get_public_shares()
    verified = v.verify_signature(sig, wrong_pub, m)
    assert not verified

    # tamper message
    corrupt_m = m + b"\x00"
    verified = v.verify_signature(sig, pub, corrupt_m)
    assert not verified
