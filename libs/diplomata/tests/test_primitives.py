from diplomata.elgamal import ElGamalCrypto
from diplomata.primitives import *

CURVE = 'P-384'

cryptosys = ElGamalCrypto(curve=CURVE)

def test_signature():
    signer = Signer()

    x = cryptosys.generate_key()    # private
    y = x.public_key()              # public
    m = b"This is a message"        # message

    # success
    sig = signer.sign(x, m)
    verified = signer.verify_signature(sig, y, m)
    assert verified

    # corrupt signature
    corrupt_sig = sig + b"\x00"
    verified = signer.verify_signature(corrupt_sig, y, m)
    assert not verified

    # use wrong key
    wrong_y = cryptosys.generate_key().public_key()
    verified = signer.verify_signature(sig, wrong_y, m)
    assert not verified

    # tamper message
    corrupt_m = m + b"\x00"
    verified = signer.verify_signature(sig, y, corrupt_m)
    assert not verified
