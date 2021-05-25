import zerorpc
import json
from diplomata.protocol import KeyManager, Holder, Issuer, Verifier
from diplomata.protocol import AWARD, REQUEST, PROOF

CURVE = 'P-384'             # Cryptosystem config

km = KeyManager(CURVE)

class DiplomataRPC(object):
    def generate_keys(self):
        key = km.generate_key()
        pub = km.get_public_from_key(key)
        return {
          'private': key,
          'public': pub,
        }
    def publish_award(self, title, issuer_key):
        issuer = Issuer.create_from_key(curve=CURVE, key=issuer_key)
        s_awd, c, r = issuer.publish_award(title)
        return {
          "s_awd": s_awd,
          "c": c,
          "r": r
        }
    def publish_request(self, s_awd, holder_key, c, verifier_pub):
        holder   = Holder.create_from_key(curve=CURVE, key=holder_key)
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



s = zerorpc.Server(DiplomataRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()
