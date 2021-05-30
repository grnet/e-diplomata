import zerorpc
import json
from diplomata.protocol import KeyManager, Holder, Issuer, Verifier
from diplomata.util import *


RPC_CONFIG = {
    'flattener': True,
    'hexifier': True,
    'curve': 'P-384',
}


class RpcKeyManager(KeyManager):
    def __init__(self):
        super().__init__(**RPC_CONFIG)


class RpcHolder(Holder):

    def __init__(self, key=None):
        super().__init__(key=key, **RPC_CONFIG)


class RpcIssuer(Issuer):

    def __init__(self, key=None):
        super().__init__(key=key, **RPC_CONFIG)


class RpcVerifier(Verifier):

    def __init__(self, key=None):
        super().__init__(key=key, **RPC_CONFIG)


class DiplomataRPC(object):
    def generate_keys(self):
        km = RpcKeyManager()
        key = km.generate_keys()
        pub = km.get_public_from_key(key)
        return {
          'private': key,
          'public': pub,
        }
    def publish_award(self, title, issuer_key):
        issuer = RpcIssuer(issuer_key)
        s_awd, c, r = issuer.publish_award(title)
        return {
          's_awd': s_awd,
          'c': c,
          'r': r
        }
    def publish_request(self, s_awd, holder_key, c, verifier_pub):
        holder = RpcHolder(holder_key)
        s_req = holder.publish_request(s_awd, verifier_pub)
        return {
          's_req': s_req
        }
    def publish_proof(self, s_req, r, c, issuer_key, verifier_pub, holder_pub, s_awd):
        issuer = Issuer(issuer_key)
        s_prf, proof = issuer.publish_proof(s_req, r, c, verifier_pub)
        return {
          's_prf': s_prf,
          'proof': json.dumps(proof, indent=2)
        }
    def publish_ack(self, s_prf, title, proof, issuer_pub, verifier_key, s_req):
        verifier = Verifier(verifier_key)
        s_ack, result = verifier.publish_ack(s_prf, title, proof, issuer_pub)
        return {
          's_ack': s_ack,
          'status': 'success' if result else 'fail'
        }

km = RpcKeyManager()

# Generate keys and store them ins db
holder_key = km.generate_keys()
issuer_key = km.generate_keys()
verifier_key = km.generate_keys()

# Extract public counterparts to store in db
holder_pub = km.get_public_from_key(holder_key)
issuer_pub = km.get_public_from_key(issuer_key)
verifier_pub = km.get_public_from_key(verifier_key)

# Create parties
holder = RpcHolder(holder_key)
issuer = RpcIssuer(issuer_key)
verifier = RpcVerifier(verifier_key)

title = 'This is a qualification'

# Run protocol
s_awd, c, r = issuer.publish_award(title)
s_req = holder.publish_request(s_awd, verifier_pub)
s_prf, proof = issuer.publish_proof(s_req, r, c, verifier_pub)
s_ack, result = verifier.publish_ack(s_prf, title, proof, issuer_pub)

# import pdb; pdb.set_trace()

assert result
print(result)


s = zerorpc.Server(DiplomataRPC())
s.bind('tcp://0.0.0.0:4242')
s.run()
