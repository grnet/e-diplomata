import zerorpc
import json
from diplomata.protocol import KeyManager, Holder, Issuer, Verifier
from diplomata.util import *

CURVE = 'P-384'             # Cryptosystem config

unhex = lambda x: int(x, 16)

class Hexifier(object):

    def _hexify_ecc_point(self, pt):
        return [hex(pt[0]), hex(pt[1])]

    def _unhexify_ecc_point(self, pt):
        return [unhex(pt[0]), unhex(pt[1])]

    def _hexify_scalar(self, scalar):
        return hex(scalar)

    def _unhexify_scalar(self, scalar):
        return unhex(scalar)

    def _hexify_commitment(self, c):
        c_1, c_2 = extract_cipher(c)
        c_1 = self._hexify_ecc_point(c_1)
        c_2 = self._hexify_ecc_point(c_2)
        c = set_cipher(c_1, c_2)
        return c

    def _unhexify_commitment(self, c):
        c_1, c_2 = extract_cipher(c)
        c_1 = self._unhexify_ecc_point(c_1)
        c_2 = self._unhexify_ecc_point(c_2)
        c = set_cipher(c_1, c_2)
        return c

    def _hexify_ddh(self, ddh):
        u, v, w = ddh
        u = self._hexify_ecc_point(u)
        v = self._hexify_ecc_point(v)
        w = self._hexify_ecc_point(w)
        ddh = u, v, w
        return ddh

    def _unhexify_ddh(self, ddh):
        u, v, w = ddh
        u = self._unhexify_ecc_point(u)
        v = self._unhexify_ecc_point(v)
        w = self._unhexify_ecc_point(w)
        ddh = u, v, w
        return ddh

    def _hexify_chaum_pedersen(self, proof):
        u_comm, v_comm, s, d = extract_chaum_pedersen(proof)
        u_comm = self._hexify_ecc_point(u_comm)
        v_comm = self._hexify_ecc_point(v_comm)
        s = self._hexify_scalar(s)
        d = self._hexify_ecc_point(d)
        proof = set_chaum_pedersen(u_comm, v_comm, s, d)
        return proof

    def _unhexify_chaum_pedersen(self, proof):
        u_comm, v_comm, s, d = extract_chaum_pedersen(proof)
        u_comm = self._unhexify_ecc_point(u_comm)
        v_comm = self._unhexify_ecc_point(v_comm)
        s = self._unhexify_scalar(s)
        d = self._unhexify_ecc_point(d)
        proof = set_chaum_pedersen(u_comm, v_comm, s, d)
        return proof

    def _hexify_ddh_proof(self, ddh_proof):
        ddh, proof = extract_ddh_proof(ddh_proof)
        ddh = self._hexify_ddh(ddh)
        proof = self._hexify_chaum_pedersen(proof)
        ddh_proof = set_ddh_proof(ddh, proof)
        return ddh_proof

    def _unhexify_ddh_proof(self, ddh_proof):
        ddh, proof = extract_ddh_proof(ddh_proof)
        ddh = self._unhexify_ddh(ddh)
        proof = self._unhexify_chaum_pedersen(proof)
        ddh_proof = set_ddh_proof(ddh, proof)
        return ddh_proof

    def _hexify_nirenc(self, nirenc):
        proof_c1, proof_c2 = extract_nirenc(nirenc)
        proof_c1 = self._hexify_ddh_proof(proof_c1)
        proof_c2 = self._hexify_ddh_proof(proof_c2)
        nirenc = set_nirenc(proof_c1, proof_c2)
        return nirenc

    def _unhexify_nirenc(self, nirenc):
        proof_c1, proof_c2 = extract_nirenc(nirenc)
        proof_c1 = self._unhexify_ddh_proof(proof_c1)
        proof_c2 = self._unhexify_ddh_proof(proof_c2)
        nirenc = set_nirenc(proof_c1, proof_c2)
        return nirenc

    def _hexify_proof(self, proof):
        c_r, decryptor, nirenc, niddh = extract_proof(proof)
        c_r = self._hexify_commitment(c_r)
        nirenc = self._hexify_nirenc(nirenc)
        proof = set_proof(c_r, decryptor, nirenc, niddh)
        return proof

    def _unhexify_proof(self, proof):
        c_r, decryptor, nirenc, niddh = extract_proof(proof)
        c_r = self._unhexify_commitment(c_r)
        nirenc = self._unhexify_nirenc(nirenc)
        proof = set_proof(c_r, decryptor, nirenc, niddh)
        return proof



class RpcKeyManager(object):

    def __init__(self, curve='P-384'):
        self._key_manager = KeyManager(curve=curve)

    def generate_keys(self):
        return self._key_manager.generate_keys(serialized=True, 
            adapted=True)

    def get_public_from_key(self, key):
        return self._key_manager.get_public_from_key(key, 
            serialized=True, from_adapted=True, to_adapted=True)

    def radapt_key(self, key):
        return self._key_manager._radapt_key(key)


class RpcHolder(Hexifier):

    def __init__(self, curve='P-384', key=None):
        self._holder = Holder(curve=curve, key=key)

    @classmethod
    def create_from_key(cls, key, curve='P-384'):
        key = RpcKeyManager(curve=curve).radapt_key(key)
        return cls(curve=curve, key=key)

    def publish_request(self, s_awd, verifier_pub):
        s_req = self._holder.publish_request(s_awd, verifier_pub)
        return s_req
        

class RpcIssuer(Hexifier):

    def __init__(self, curve='P-384', key=None):
        self._issuer = Issuer(curve=curve, key=key)

    @classmethod
    def create_from_key(cls, key, curve='P-384'):
        key = RpcKeyManager(curve=curve).radapt_key(key)
        return cls(curve=curve, key=key)

    def publish_award(self, title):
        s_awd, c, r = self._issuer.publish_award(title)
        c = self._hexify_commitment(c)
        r = self._hexify_scalar(r)
        return s_awd, c, r

    def publish_proof(self, s_req, r, c, verifier_pub):
        r = self._unhexify_scalar(r)
        c = self._unhexify_commitment(c)
        s_prf, proof = self._issuer.publish_proof(s_req, r, c, verifier_pub)
        proof = self._hexify_proof(proof)
        return s_prf, proof

class RpcVerifier(Hexifier):

    def __init__(self, curve='P-384', key=None):
        self._verifier = Verifier(curve=curve, key=key)

    @classmethod
    def create_from_key(cls, key, curve='P-384'):
        key = RpcKeyManager(curve=curve).radapt_key(key)
        return cls(curve=curve, key=key)

    def publish_ack(self, s_prf, title, proof, issuer_pub):
        proof = self._unhexify_proof(proof)
        s_ack, result = self._verifier.publish_ack(s_prf, title, proof,
                issuer_pub)
        return s_ack, result


class DiplomataRPC(object):
    def generate_keys(self):
        km = RpcKeyManager(CURVE)
        key = km.generate_key()
        pub = km.get_public_from_key(key)
        return {
          'private': key,
          'public': pub,
        }
    def publish_award(self, title, issuer_key):
        issuer = RpcIssuer.create_from_key(curve=CURVE, key=issuer_key)
        s_awd, c, r = issuer.publish_award(title)
        return {
          "s_awd": s_awd,
          "c": c,
          "r": r
        }
    def publish_request(self, s_awd, holder_key, c, verifier_pub):
        holder = RpcHolder.create_from_key(curve=CURVE, key=holder_key)
        s_req = holder.publish_request(s_awd, verifier_pub)
        return {
          "s_req": s_req
        }
    def publish_proof(self, s_req, r, c, issuer_key, verifier_pub, holder_pub, s_awd):
        issuer   = Issuer.create_from_key(curve=CURVE, key=issuer_key)
        s_prf, proof = issuer.publish_proof(s_req, r, c, verifier_pub)
        return {
          "s_prf": s_prf,
          "proof": json.dumps(proof, indent=2)
        }
    def publish_ack(self, s_prf, title, proof, issuer_pub, verifier_key, s_req):
        verifier = Verifier.create_from_key(curve=CURVE, key=verifier_key)
        s_ack, result = verifier.publish_ack(s_prf, title, proof, issuer_pub)
        return {
          "s_ack": s_ack,
          "status": 'success' if result else 'fail'
        }

km = RpcKeyManager(CURVE)

# Generate keys and store them ins db
holder_key = km.generate_keys()
issuer_key = km.generate_keys()
verifier_key = km.generate_keys()

# Extract public counterparts to store in db
holder_pub = km.get_public_from_key(holder_key)
issuer_pub = km.get_public_from_key(issuer_key)
verifier_pub = km.get_public_from_key(verifier_key)

# Create involved parties from keys
holder = RpcHolder.create_from_key(curve=CURVE, key=holder_key)
issuer = RpcIssuer.create_from_key(curve=CURVE, key=issuer_key)
verifier = RpcVerifier.create_from_key(curve=CURVE, key=verifier_key)

title = 'This is a qualification'

# Run protocol
s_awd, c, r = issuer.publish_award(title)
s_req = holder.publish_request(s_awd, verifier_pub)
s_prf, proof = issuer.publish_proof(s_req, r, c, verifier_pub)
s_ack, result = verifier.publish_ack(s_prf, title, proof, issuer_pub)

assert result
print(result)


s = zerorpc.Server(DiplomataRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()
