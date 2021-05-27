from abc import ABCMeta, abstractmethod

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



from Cryptodome.PublicKey.ECC import EccPoint
from Cryptodome.Math.Numbers import Integer
from Cryptodome.PublicKey import ECC
from diplomata.util import *

class _ElGamalSerializer(_Adaptor):

    def __init__(self, curve):
        self.curve = curve

    def _adapt_scalar(self, scalar, reverse):
        if not reverse:
            return int(scalar)
        else:
            return Integer(scalar)

    def _adapt_ecc_point(self, pt, reverse):
        if not reverse:
            return [int(_) for _ in pt.xy]
        else:
            return EccPoint(*pt, curve=self.curve.desc)

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
            point_x=ecc_key['x'],
            point_y=ecc_key['y'],
            d=ecc_key['d'],
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
