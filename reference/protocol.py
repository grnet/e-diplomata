from util import *


class Party(object):

    def __init__(self, curve='P-384'):
        self.curve = gen_curve(curve)
        self.key = self._keygen(self.curve)
        self.signer = self._create_signer(self.key['ecc'])

    @staticmethod
    def _keygen(curve):
        return {
            'ecc': ECC.generate(curve=curve.desc),
            'nacl': PrivateKey.generate(),
        }

    @staticmethod
    def _create_signer(key):
        return DSS.new(key, 'fips-186-3')


    # Algebra layer

    def serialize_ecc_point(self, pt):
        return [int(_) for _ in pt.xy]
    
    def deserialize_ecc_point(self, pt):
        return EccPoint(*pt, curve=self.curve.desc)
    
    def serialize_factor(self, factor):
        return int(factor)
    
    def deserialize_factor(self, factor):
        return Integer(factor)

    def generate_randomness(self):
        return Integer.random_range(
            min_inclusive=1, 
            max_exclusive=self.curve.order
        )


    # Key management

    def get_public_shares(self):
        return {
            'ecc': self.key['ecc'].pointQ,
            'nacl': self.key['nacl'].public_key,
        }


    # DSA (Digital Signature Algorithm)

    def sign(self, payload):
        hc = SHA384.new(payload)
        signature = self.signer.sign(hc)
        return signature

    def verify_signature(self, s):
        pass


    # Symmetric (common secret) encryption

    def encrypt(self, content, receiver_pub):
        """
        Encrypt using common secret (currently a wrapper around box.encrypt)

        content: bytes
        """
        box = Box(self.key['nacl'], receiver_pub['nacl'])
        cipher = box.encrypt(content)
        return cipher

    def decrypt(self, cipher, sender_pub):
        """
        Decrypt using common secret (currently a wrapper around box.decrypt)

        return: bytes
        """
        box = Box(self.key['nacl'], sender_pub['nacl'])
        content = box.decrypt(cipher)
        return content


    # ElGamal encryption

    def set_cipher(self, c1, c2):
        cipher = {
            'c1': c1,
            'c2': c2,
        }
        return cipher
    
    def extract_cipher(self, cipher):
        c1 = cipher['c1']
        c2 = cipher['c2']
        return c1, c2
        
    def elgamal_encrypt(self, public, m):
        g = self.curve.G
        r = self.generate_randomness()
        cipher = self.set_cipher(
            r * g,
            m * g + r * public['ecc'],
        )
        return cipher, r

    # TODO: Make clear the meaning of this function with respet to ElGamal
    # encryption and rename appropriately
    def commit(self, public, t):
        ht = hash_into_integer(t)                           # H(t)
        commitment, r = self.elgamal_encrypt(public, ht)    # (r * g, H(t) * g + r * I), r
        return commitment, r
    
    def elgamal_decrypt(self, cipher, table):
        a, b = self.extract_cipher(cipher)
        v = b + (self.key['ecc'].d * (-a))      # TODO
        return table[(str(v.x), str(v.y))]
    
    def elgamal_reencrypt(self, public, cipher):    
        g = self.curve.G
        r = self.generate_randomness()
        c1, c2 = self.extract_cipher(cipher)
        cipher = self.set_cipher(
            r * g + c1,
            c2 + r * public['ecc'],
        )
        return cipher, r
    
    def elgamal_drenc(self, cipher, decryptor):
        _, c2 = self.extract_cipher(cipher)
        m = c2 + (-decryptor)
        return m


    # Chaum-Pedersen protocol

    def serialize_ddh(self, ddh):
        return list(map(self.serialize_ecc_point, ddh))
    
    def deserialize_ddh(self, ddh):
        return tuple(map(
            self.deserialize_ecc_point, 
            ddh
        ))

    def set_proof(self, u_comm, v_comm, s, d):
        return {
            'u_comm': u_comm,
            'v_comm': v_comm,
            's': s,
            'd': d,
        }

    def serialize_proof(self, proof):
        u_comm, v_comm, s, d = self.extract_proof(proof)
        return {
            'u_comm': self.serialize_ecc_point(u_comm),
            'v_comm': self.serialize_ecc_point(v_comm),
            's': self.serialize_factor(s),
            'd': self.serialize_ecc_point(d)
        }
    
    def deserialize_proof(self, proof):
        u_comm, v_comm, s, d = self.extract_proof(proof)
        return {
            'u_comm': self.deserialize_ecc_point(u_comm),
            'v_comm': self.deserialize_ecc_point(v_comm),
            's': self.deserialize_factor(s),
            'd': self.deserialize_ecc_point(d),
        }
    
    def extract_proof(self, proof):
        u_comm = proof['u_comm']
        v_comm = proof['v_comm']
        s = proof['s']
        d = proof['d']
        return u_comm, v_comm, s, d

    def set_ddh_proof(self, ddh, proof):
        return {
            'ddh': ddh,
            'proof': proof
        }
    
    def extract_ddh_proof(self, ddh_proof):
        ddh = ddh_proof['ddh']
        proof = ddh_proof['proof']
        return ddh, proof

    def serialize_ddh_proof(self, ddh_proof):
        ddh, proof = self.extract_ddh_proof(ddh_proof)
        return {
            'ddh': self.serialize_ddh(ddh),
            'proof': self.serialize_proof(proof),
        }
    
    def deserialize_ddh_proof(self, ddh_proof):
        ddh, proof = self.extract_ddh_proof(ddh_proof)
        return {
            'ddh': self.deserialize_ddh(ddh),
            'proof': self.deserialize_proof(proof),
        }

    def generate_chaum_pedersen(self, ddh, z, *extras):
        g = self.curve.G
        r = self.generate_randomness();
    
        u, v, w = ddh
    
        u_comm = r * u                                      # u commitment
        v_comm = r * g                                      # g commitment
    
        c = fiat_shamir(u, v, w, u_comm, v_comm, *extras)   # challenge
    
        s = (r + c * z) % self.curve.order                  # response
        d = z * u
    
        proof = self.set_proof(u_comm, v_comm, s, d)
        return proof
    
    def verify_chaum_pedersen(self, ddh, proof, *extras):
        g = self.curve.G
        u, v, w = ddh
        u_comm, v_comm, s, d = self.extract_proof(proof)
        c = fiat_shamir(u, v, w, u_comm, v_comm,  *extras)   # challenge
        return (s * u == u_comm + c * d) and \
               (s * g == v_comm + c * v)


    # Other primitives

    # TODO: Remove it when chaum-pedersen infra is ready
    def auxiliary_chaum_pedersen_proof(self, u, w):
        pub = ecc_pub_key(self.key['ecc'])    # public; TODO
        v = pub
        z = int(self.key['ecc'].d)              # secret; TODO
        extras = (pub,)
        proof = self.generate_chaum_pedersen((u, v, w), z, *extras)
        return proof

    def set_nirenc(self, proof_c1, proof_c2):
        return {
            'proof_c1': proof_c1,
            'proof_c2': proof_c2,
        }

    def extract_nirenc(self, nirenc):
        proof_c1 = nirenc['proof_c1']
        proof_c2 = nirenc['proof_c2']
        return proof_c1, proof_c2


class Holder(Party):

    def publish_request(self, s_awd, verifier_pub):
        pub = verifier_pub['ecc']
        payload = (f'REQUEST s_awd={s_awd} ver_pub={pub}').encode('utf-8')
        s_req = self.sign(payload)
        return s_req


class Issuer(Party):

    def commit_to_document(self, document):
        return self.commit(
            self.get_public_shares(),           # TODO
            document
        )

    def publish_award(self, t):
        c, r = self.commit_to_document(t)   # c1, c2

        c1, c2 = self.extract_cipher(c)
        payload = f'AWARD c1={c1.xy} c2={c2.xy}'.encode('utf-8')

        s_awd = self.sign(payload)
        return s_awd, c, r

    def reencrypt_commitment(self, c):
        c_r, r_r = self.elgamal_reencrypt(
            self.get_public_shares(),           # TODO
            c,
        )
        return c_r, r_r

    def create_decryptor(self, r1, r2, verifier_pub):
        r_tilde = r1 + r2
        decryptor = ecc_pub_key(self.key['ecc']) * r_tilde              # TODO

        enc_decryptor = self.encrypt(
            str(decryptor.xy).encode('utf-8'),
            verifier_pub
        )

        return decryptor, enc_decryptor

    def generate_nirenc(self, c, c_r, verifier_pub):
        c1  , c2   = self.extract_cipher(c)
        c1_r, c2_r = self.extract_cipher(c_r)

        # TODO:
        pub = ecc_pub_key(self.key['ecc'])
        proof_c1 = self.set_ddh_proof(
            (c1, pub, c1_r),
            self.auxiliary_chaum_pedersen_proof(c1, c1_r)   # TODO: Remove
        )
        proof_c2 = self.set_ddh_proof(
            (c2, pub, c2_r),
            self.auxiliary_chaum_pedersen_proof(c2, c2_r)   # TODO: Remove
        )

        nirenc = self.set_nirenc(proof_c1, proof_c2)
        return nirenc

    def serialize_nirenc(self, nirenc):
        proof_c1, proof_c2 = self.extract_nirenc(nirenc)
        return {
            'proof_c1': self.serialize_ddh_proof(proof_c1),
            'proof_c2': self.serialize_ddh_proof(proof_c2),
        }

    def generate_niddh(self, r1, r2, verifier_pub):
        # TODO
        g = self.curve.G
        g_r = g * r1
        g_r_r = g * r2
        pub = ecc_pub_key(self.key['ecc'])    # public; TODO
        niddh = self.set_ddh_proof(
            (g_r, pub, g_r_r),
            self.auxiliary_chaum_pedersen_proof(g_r, g_r_r)
        )
        niddh = self.serialize_ddh_proof(niddh)

        enc_niddh = self.encrypt(
            json.dumps(niddh).encode('utf-8'),
            verifier_pub
        )
        return niddh, enc_niddh


    def publish_proof(self, r, c, s_req, verifier_pub):
        # Re-encrypt commitment
        c_r, r_r = self.reencrypt_commitment(c)

        # Create and encrypt decryptor
        decryptor, enc_decryptor = self.create_decryptor(r, r_r, verifier_pub)

        # create NIRENC
        nirenc = self.generate_nirenc(c, c_r, verifier_pub)
        nirenc = self.serialize_nirenc(nirenc)

        # Create and encrypt NIDDH of the above decryptor addressed to VERIFIER
        niddh, enc_niddh = self.generate_niddh(r, r_r, verifier_pub)

        # Create PROOF tag
        nirenc_str = json.dumps(nirenc)
        c_r_1, c_r_2 = self.extract_cipher(c_r)
        payload = (f'PROOF s_req={s_req} c_r=({c_r_1.xy, c_r_2.xy}) '
                   f'{nirenc_str} {enc_decryptor} '
                   f'{enc_niddh}'.encode('utf-8'))
        s_prf = self.sign(payload)

        return (s_prf, c_r, nirenc, enc_decryptor, enc_niddh)


class Verifier(Party):

    def retrieve_decryptor(self, issuer_pub, enc_decryptor):
        dec_decryptor = self.decrypt(enc_decryptor, issuer_pub).decode('utf-8')

        extract_coords = re.match(r'^\D*(\d+)\D+(\d+)\D*$', dec_decryptor)
        x_affine = int(extract_coords.group(1))
        y_affine = int(extract_coords.group(2))
        # TODO: Raise exception for caller?
        if not extract_coords:
            payload = f'FAIL {s_prf}'.encode('utf-8')
            s_ack = verifier.sign(payload)
            return s_ack
        decryptor = ECC.EccPoint(x_affine, y_affine, curve=self.curve.desc)
        return decryptor

    def decrypt_commitment(self, c_r, decryptor):
        dec_m = self.elgamal_drenc(c_r, decryptor)
        return dec_m

    def check_message_integrity(self, message, dec_m):
        """
        Checks that dec_m coincides with the hash of message,
        seen as ECC points
        """
        g = self.curve.G
        h = hash_into_integer(message)
        h_ecc_point = g * h
        return dec_m == h_ecc_point

    def deserialize_nirenc(self, nirenc):
        proof_c1, proof_c2 = self.extract_nirenc(nirenc)
        return {
            'proof_c1': self.deserialize_ddh_proof(proof_c1),
            'proof_c2': self.deserialize_ddh_proof(proof_c2),
        }

    def verify_nirenc(self, nirenc, issuer_pub):

        nirenc = self.deserialize_nirenc(nirenc)
        proof_c1, proof_c2 = self.extract_nirenc(nirenc)
        extras = (issuer_pub['ecc'],)

        ddh, proof = self.extract_ddh_proof(proof_c1)
        check_proof_c1 = self.verify_chaum_pedersen(ddh, proof, *extras)
        assert check_proof_c1   # TODO: Remove

        ddh, proof = self.extract_ddh_proof(proof_c2)
        check_proof_c2 = self.verify_chaum_pedersen(ddh, proof, *extras)
        assert check_proof_c2   # TODO: Remove

        return check_proof_c1 and check_proof_c2

    def verify_niddh(self, enc_niddh, issuer_pub):
        niddh = json.loads(self.decrypt(enc_niddh, issuer_pub).decode('utf-8')) # TODO
        niddh = self.deserialize_ddh_proof(niddh)
        ddh, proof = self.extract_ddh_proof(niddh)
        extras = (issuer_pub['ecc'],)                           # TODO
        return self.verify_chaum_pedersen(ddh, proof, *extras)


    def publish_ack(self, s_prf, m, c_r, nirenc, enc_decryptor, enc_niddh, issuer_pub):
    
        # VERIFIER etrieves decryptor created for them by ISSUER
        decryptor = self.retrieve_decryptor(issuer_pub, enc_decryptor)
    
        # VERIFIER decrypts the re-encrypted commitment
        dec_m = self.decrypt_commitment(c_r, decryptor)
    
        # VERIFIER checks content of document
        check_m_integrity = self.check_message_integrity(m, dec_m)
        assert check_m_integrity    # TODO: Remove
    
        # VERIFIER verifies NIRENC proof
        check_nirenc = self.verify_nirenc(nirenc, issuer_pub)
        assert check_nirenc         # TODO: Remove
    
        # VERIFIER verifies NIDDH proof
        check_niddh = self.verify_niddh(enc_niddh, issuer_pub)
        assert check_niddh          # TODO: Remove
    
        # VERIFIER creates TAG
        if not all((
            check_m_integrity, 
            check_nirenc, 
            check_niddh,
        )):
            # Some check failed; reject proof
            payload = f'FAIL {s_prf}'.encode('utf-8')
            s_ack = self.sign(payload)
            return s_ack
        else:
            # All checks succeded, acknowledge proof
            payload = f'ACK {s_prf}'.encode('utf-8')
            s_ack = self.sign(payload)
            return s_ack
