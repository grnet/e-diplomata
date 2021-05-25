import zerorpc
import json
from diplomata.protocol import (
    KeyManager as _KeyManager,
    Holder as _Holder,
    Issuer as _Issuer,
    Verifier as _Verifier,
)

CURVE = 'P-384'             # Cryptosystem config

KeyManager = _KeyManager
Holder = _Holder
Issuer = _Issuer
Verifier = _Verifier


class RpcKeyManager(object):

    def __init__(self, curve='P-384'):
        self._key_manager = KeyManager(curve=curve)

    def generate_keys(self):
        return self._key_manager.generate_keys(serialized=True, 
            adapted=True)

    def get_public_from_key(self, key):
        return self._key_manager.get_public_from_key(key, 
            serialized=True, from_adapted=True, to_adapted=True)


class RpcHolder(object):

    def __init__(self, curve='P-384', key=None):
        self._holder = Holder(curve=curve, key=key)

    @classmethod
    def create_from_key(cls, key, curve='P-384'):
        return cls(curve=curve, key=key)

    def publish_request(self, s_awd, verifier_pub):
        s_req = self._holder.publish_request(s_awd, verifier_pub)
        return s_req
        

class RpcIssuer(object):

    def __init__(self, curve='P-384', key=None):
        self._issuer = Issuer(curve=curve, key=key)

    @classmethod
    def create_from_key(cls, key, curve='P-384'):
        return cls(curve=curve, key=key)

    def publish_award(self, title):
        s_awd, c, r = self._issuer.publish_award(title)
        return s_awd, c, r

    def publish_proof(self, s_req, r, c, verifier_pub):
        s_prf, proof = self._issuer.publish_proof(s_req, r, c, verifier_pub)
        return s_prf, proof

class RpcVerifier(object):

    def __init__(self, curve='P-384', key=None):
        self._verifier = Verifier(curve=curve, key=key)

    @classmethod
    def create_from_key(cls, key, curve='P-384'):
        return cls(curve=curve, key=key)

    def publish_ack(self, s_prf, title, proof, issuer_pub):
        s_ack, result = self._verifier.publish_ack(s_prf, title, proof,
                issuer_pub)
        return s_ack, result


km = RpcKeyManager(CURVE)


class DiplomataRPC(object):
    def generate_keys(self):
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


holder_key = km.generate_keys()
issuer_key = km.generate_keys()
verifier_key = km.generate_keys()

holder_pub = km.get_public_from_key(holder_key)
issuer_pub = km.get_public_from_key(issuer_key)
verifier_pub = km.get_public_from_key(verifier_key)

holder = RpcHolder.create_from_key(
    km._key_manager._radapt_key(holder_key)
)
issuer = RpcIssuer.create_from_key(
    km._key_manager._radapt_key(issuer_key),
)
verifier = RpcVerifier.create_from_key(
    km._key_manager._radapt_key(verifier_key),
)

title = 'This is a qualification'

s_awd, c, r = issuer.publish_award(title)
s_req = holder.publish_request(s_awd, verifier_pub)
s_prf, proof = issuer.publish_proof(s_req, r, c, verifier_pub)
s_ack, result = verifier.publish_ack(s_prf, title, proof, issuer_pub)
print(result)


s = zerorpc.Server(DiplomataRPC())
s.bind("tcp://0.0.0.0:4243")
s.run()
