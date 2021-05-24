import zerorpc
import json
from diplomata.protocol import KeyGenerator, Holder, Issuer, Verifier
from diplomata.protocol import AWARD, REQUEST, PROOF

CURVE = 'P-384'             # Cryptosystem config

kg = KeyGenerator(CURVE)

class DiplomataRPC(object):
    def generate_keys(self):
        print(kg.generate_keys())
        return {
          'key': 'as'
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
        payload = holder.create_tag(AWARD, c=c)
        assert holder.verify_signature(s_awd, issuer_pub, payload)
        s_req = holder.publish_request(s_awd, verifier_pub)
        return {
          "s_req": s_req
        }
    def publish_proof(self, s_req, r, c, issuer_key, verifier_pub, holder_pub, s_awd):
        issuer   = Issuer.create_from_key(curve=CURVE, key=issuer_key)
        payload = issuer.create_tag(REQUEST, s_awd=s_awd, verifier=verifier_pub)
        assert issuer.verify_signature(s_req, holder_pub, payload)
        s_prf, proof = issuer.publish_proof(s_req, r, c, verifier_pub)
        return {
          "s_prf": s_prf,
          "proof": json.dumps(proof, indent=2)
        }
    def publish_ack(self, s_prf, title, proof, issuer_pub, verifier_key, s_req):
        verifier = Verifier.create_from_key(curve=CURVE, key=verifier_key)
        payload = verifier.create_tag(PROOF, s_req=s_req, **proof)
        assert verifier.verify_signature(s_prf, issuer_pub, payload)
        s_ack, result = verifier.publish_ack(s_prf, title, proof, issuer_pub)
        return {
          "s_ack": s_ack,
          "status": 'success' if result else 'fail'
        }



s = zerorpc.Server(DiplomataRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()