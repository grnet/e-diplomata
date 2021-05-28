from abc import ABCMeta, abstractmethod
from Cryptodome.PublicKey.ECC import EccPoint
from Cryptodome.Math.Numbers import Integer
from Cryptodome.PublicKey import ECC
from nacl.public import PrivateKey as _NaclKey, PublicKey as _NaclPublicKey
from diplomata.util import *


class _Adaptor(metaclass=ABCMeta):

    @abstractmethod
    def _adapt_scalar(self, scalar, reverse):
        """
        """

    @abstractmethod
    def _adapt_ecc_point(self, pt, reverse):
        """
        """

    def _adapt_cipher(self, cipher, reverse):
        c1, c2 = extract_cipher(cipher)
        c1 = self._adapt_ecc_point(c1, reverse=reverse)
        c2 = self._adapt_ecc_point(c2, reverse=reverse)
        cipher = set_cipher(c1, c2)
        return cipher

    def _adapt_ddh(self, ddh, reverse):
        u, v, w = ddh
        u = self._adapt_ecc_point(u, reverse=reverse)
        v = self._adapt_ecc_point(v, reverse=reverse)
        w = self._adapt_ecc_point(w, reverse=reverse)
        ddh = [u, v, w]
        return ddh

    def _adapt_chaum_pedersen(self, proof, reverse):
        u_comm, v_comm, s, d = extract_chaum_pedersen(proof)
        u_comm = self._adapt_ecc_point(u_comm, reverse=reverse)
        v_comm = self._adapt_ecc_point(v_comm, reverse=reverse)
        s = self._adapt_scalar(s, reverse=reverse)
        d = self._adapt_ecc_point(d, reverse=reverse)
        proof = set_chaum_pedersen(u_comm, v_comm, s, d)
        return proof

    def _adapt_ddh_proof(self, ddh_proof, reverse):
        ddh, proof = extract_ddh_proof(ddh_proof)
        ddh = self._adapt_ddh(ddh, reverse=reverse)
        proof = self._adapt_chaum_pedersen(proof, reverse=reverse)
        ddh_proof = set_ddh_proof(ddh, proof)
        return ddh_proof

    def _adapt_nirenc(self, nirenc, reverse):
        proof_c1, proof_c2 = extract_nirenc(nirenc)
        proof_c1 = self._adapt_ddh_proof(proof_c1, reverse=reverse)
        proof_c2 = self._adapt_ddh_proof(proof_c2, reverse=reverse)
        nirenc = set_nirenc(proof_c1, proof_c2)
        return nirenc

    def _adapt_niddh(self, niddh, reverse):
        return self._adapt_ddh_proof(niddh, reverse=reverse)

    def _adapt_proof(self, proof, reverse):
        c_r, decryptor, nirenc, niddh = extract_proof(proof)
        c_r = self._adapt_cipher(c_r, reverse=reverse)
        nirenc = self._adapt_nirenc(nirenc, reverse=reverse)
        proof = set_proof(c_r, decryptor, nirenc, niddh)
        return proof

    def _adapt_signature(self, signature, reverse):
        if not reverse:
            return signature.hex()
        else:
            return bytes.fromhex(signature)


class _ElGamalSerializer(_Adaptor):

    def __init__(self, curve, hexifier=True):
        self.curve = gen_curve(curve)
        self.hexifier = hexifier

    def _hexify(self, x):
        return hex(x) if self.hexifier else x

    def _unhexify(self, x):
        return int(x.lstrip('0x'), 16) if self.hexifier else x

    def _adapt_scalar(self, scalar, reverse):
        if not reverse:
            return self._hexify(int(scalar))
        else:
            return Integer(self._unhexify(scalar))

    def _adapt_ecc_point(self, pt, reverse):
        if not reverse:
            return [self._hexify(int(_)) for _ in pt.xy]
        else:
            return EccPoint(*map(self._unhexify, pt), curve=self.curve.desc)

    def serialize_scalar(self, scalar):
        return self._adapt_scalar(scalar, reverse=False)
    
    def deserialize_scalar(self, scalar):
        return self._adapt_scalar(scalar, reverse=True)
    
    def serialize_ecc_point(self, pt):
        return self._adapt_ecc_point(pt, reverse=False)
    
    def deserialize_ecc_point(self, pt):
        return self._adapt_ecc_point(pt, reverse=True)

    def serialize_cipher(self, cipher):
        return self._adapt_cipher(cipher, reverse=False)

    def deserialize_cipher(self, cipher):
        return self._adapt_cipher(cipher, reverse=True)

    def serialize_ddh(self, ddh):
        return self._adapt_ddh(ddh, reverse=False)
    
    def deserialize_ddh(self, ddh):
        return self._adapt_ddh(ddh, reverse=True)

    def serialize_chaum_pedersen(self, proof):
        return self._adapt_chaum_pedersen(proof, reverse=False)
    
    def deserialize_chaum_pedersen(self, proof):
        return self._adapt_chaum_pedersen(proof, reverse=True)

    def serialize_ddh_proof(self, ddh_proof):
        return self._adapt_ddh_proof(ddh_proof, reverse=False)
    
    def deserialize_ddh_proof(self, ddh_proof):
        return self._adapt_ddh_proof(ddh_proof, reverse=True)

    def serialize_nirenc(self, nirenc):
        return self._adapt_nirenc(nirenc, reverse=False)
    
    def deserialize_nirenc(self, nirenc):
        return self._adapt_nirenc(nirenc, reverse=True)

    def serialize_niddh(self, niddh):
        return self._adapt_niddh(niddh, reverse=False)

    def deserialize_niddh(self, niddh):
        return self._adapt_niddh(niddh, reverse=True)

    def serialize_proof(self, proof):
        return self._adapt_proof(proof, reverse=False)

    def deserialize_proof(self, proof):
        return self._adapt_proof(proof, reverse=True)

    def serialize_signature(self, signature):
        return self._adapt_signature(signature, reverse=False)

    def deserialize_signature(self, signature):
        return self._adapt_signature(signature, reverse=True)


class _ElGamalKeySerializer(_ElGamalSerializer):

    def serialize_ecc_key(self, ecc_key):
        pub  = self.serialize_ecc_point(ecc_key.pointQ)
        priv = self.serialize_scalar(ecc_key.d)
        return {
            'x': pub[0],
            'y': pub[1],
            'd': priv,
        }

    def deserialize_ecc_key(self, ecc_key):
        return ECC.construct(
            curve=self.curve.desc,
            point_x=self._unhexify(ecc_key['x']),
            point_y=self._unhexify(ecc_key['y']),
            d=self._unhexify(ecc_key['d']),
        )

    def serialize_ecc_public(self, pub):
        return self.serialize_ecc_point(pub)

    def deserialize_ecc_public(self, pub, for_signature=False):
        if for_signature is True:
            return ECC.construct(
                curve=self.curve.desc, 
                point_x=pub[0], 
                point_y=pub[1],
            )
        return self.deserialize_ecc_point(pub) 


class _KeySerializer(_ElGamalKeySerializer):

    def _serialize_nacl_key(self, nacl_key):
        return nacl_key._private_key.hex()

    def _deserialize_nacl_key(self, nacl_key):
        return _NaclKey(private_key=bytes.fromhex(nacl_key))

    def _serialize_nacl_public(self, pub):
        return bytes(pub).hex()

    def _deserialize_nacl_public(self, pub):
        return _NaclPublicKey(bytes.fromhex(pub))

    def _adapt_key(self, key):
        ecc_key, nacl_key = extract_keys(key)
        key = [
            ecc_key['x'],
            ecc_key['y'],
            ecc_key['d'],
            nacl_key,
        ]
        return key

    def _radapt_key(self, key):
        ecc_key = {
            'x': key[0],
            'y': key[1],
            'd': key[2],
        }
        nacl_key = key[3]
        key = set_keys(ecc_key, nacl_key)
        return key

    def _serialize_key(self, key, adapted=True):
        ecc_key, nacl_key = extract_keys(key)
        ecc_key  = self.serialize_ecc_key(ecc_key)
        nacl_key = self._serialize_nacl_key(nacl_key)
        key = set_keys(ecc_key, nacl_key)
        if adapted is True:
            key = self._adapt_key(key)
        return key

    def _deserialize_key(self, key, from_adapted=False):
        if from_adapted:
            key = self._radapt_key(key)
        ecc_key, nacl_key = extract_keys(key)
        ecc_key  = self.deserialize_ecc_key(ecc_key)
        nacl_key = self._deserialize_nacl_key(nacl_key)
        key = set_keys(ecc_key, nacl_key)
        return key

    def deserialize_public_shares(self, public, from_adapted=True):
        if from_adapted is True:
            public = self._radapt_public_shares(public)
        ecc_pub, nacl_pub = extract_keys(public)
        ecc_pub = self.deserialize_ecc_public(ecc_pub)
        nacl_pub = self._deserialize_nacl_public(nacl_pub)
        public = set_keys(ecc_pub, nacl_pub)
        return public
