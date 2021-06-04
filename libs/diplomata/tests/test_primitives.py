from diplomata.elgamal import ElGamalCrypto
from diplomata.primitives import *

CURVE = 'P-384'
cryptosys = ElGamalCrypto(curve=CURVE)

def test_reencryption_proof():

    # setup
    prover = Prover(curve=CURVE)
    verifier = Verifier(curve=CURVE)
    g = cryptosys.generator
    x = cryptosys.random_scalar()       # private
    y = x * g                           # public
    m = cryptosys.random_scalar() * g   # message
    c  , r   = prover._encrypt(y, m)
    c_r, r_r = prover._reencrypt(y, c)

    # success
    nirenc = prover.prove_reencryption(c, c_r, r_r, y)
    verified = verifier.verify_ddh_proof(nirenc, y)
    assert verified

    # prove with wrong public
    y_corrupt = (x + 1) * g
    nirenc = prover.prove_reencryption(c, c_r, r_r, y_corrupt)
    verified = verifier.verify_ddh_proof(nirenc, y)
    assert not verified

    # verify with wrong public
    y_corrupt = (x + 1) * g
    nirenc = prover.prove_reencryption(c, c_r, r_r, y)
    verified = verifier.verify_ddh_proof(nirenc, y_corrupt)
    assert not verified

    # prove with wrong randomness
    r_r_corrupt = r_r + 1
    nirenc = prover.prove_reencryption(c, c_r, r_r_corrupt, y)
    verified = verifier.verify_ddh_proof(nirenc, y) # y_corrupt
    assert not verified

    # prove for different initial cipher
    c_corrupt, _ = prover._encrypt(y, m)
    nirenc = prover.prove_reencryption(c_corrupt, c_r, r_r, y)
    verified = verifier.verify_ddh_proof(nirenc, y)
    assert not verified

    # prove for different re-encryption
    c_r_corrupt, _ = prover._reencrypt(y, c)
    nirenc = prover.prove_reencryption(c, c_r_corrupt, r_r, y)
    verified = verifier.verify_ddh_proof(nirenc, y)
    assert not verified

   
def test_decryption_proof():

    # setup
    prover = Prover(curve=CURVE)
    verifier = Verifier(curve=CURVE)
    g = cryptosys.generator
    x = cryptosys.random_scalar()       # private
    y = x * g                           # public
    m = cryptosys.random_scalar() * g   # message
    c, r = prover._encrypt(y, m)
    d = prover._create_decryptor(r, y)

    # success
    niddh = prover.prove_decryption(c, d, r, y)
    verified = verifier.verify_ddh_proof(niddh, y)
    assert verified

    # prove with wrong public
    y_corrupt = (x + 1) * g
    niddh = prover.prove_decryption(c, d, r, y_corrupt)
    verified = verifier.verify_ddh_proof(niddh, y)
    assert not verified

    # verify with wrong public
    y_corrupt = (x + 1) * g
    niddh = prover.prove_decryption(c, d, r, y)
    verified = verifier.verify_ddh_proof(niddh, y_corrupt)
    assert not verified

    # prove with wrong randomness
    r_corrupt = r + 1
    niddh = prover.prove_decryption(c, d, r_corrupt, y)
    verified = verifier.verify_ddh_proof(niddh, y)
    assert not verified

    # prove for different cipher
    c_corrupt, _ = prover._encrypt(y, m)
    niddh = prover.prove_decryption(c_corrupt, d, r, y)
    verified = verifier.verify_ddh_proof(niddh, y)
    assert not verified

    # prove for different decryptor
    d_corrupt = prover._create_decryptor(r + 1, y)
    niddh = prover.prove_decryption(c, d_corrupt, r, y)
    verified = verifier.verify_ddh_proof(niddh, y)
    assert not verified


def test_signature():
    signer = Signer(curve=CURVE)

    g = cryptosys.generator
    x = cryptosys.generate_key()    # private
    y = x.d * g                       # public
    m = b"This is a message"        # message

    # success
    sig = signer.sign(x, m)
    verified = signer.verify_signature(sig, y, m)
    assert verified

    # corrupt signature
    sig_corrupt = sig + b"\x00"
    verified = signer.verify_signature(sig_corrupt, y, m)
    assert not verified

    # use wrong key
    y_corrupt = (x.d + 1) * g
    verified = signer.verify_signature(sig, y_corrupt, m)
    assert not verified

    # tamper message
    m_corrupt = m + b"\x00"
    verified = signer.verify_signature(sig, y, m_corrupt)
    assert not verified
