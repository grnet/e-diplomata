"""
"""

from Cryptodome.PublicKey import ECC

def gen_curve(name):
    """
    Elliptic-curve generation
    """
    return ECC._curves[name]


# El-Gamal Backend Layer Structures

def set_cipher(c1, c2):
    cipher = {
        'c1': c1,
        'c2': c2,
    }
    return cipher

def extract_cipher(cipher):
    c1 = cipher['c1']
    c2 = cipher['c2']
    return c1, c2

def set_chaum_pedersen(g_comm, u_comm, challenge, response):
    return {
        'g_comm': g_comm,
        'u_comm': u_comm,
        'challenge': challenge,
        'response': response,
    }

def extract_chaum_pedersen(proof):
    g_comm = proof['g_comm']
    u_comm = proof['u_comm']
    challenge = proof['challenge']
    response = proof['response']
    return g_comm, u_comm, challenge, response

def set_ddh_proof(ddh, proof):
    return {
        'ddh': ddh,
        'proof': proof
    }

def extract_ddh_proof(ddh_proof):
    ddh = ddh_proof['ddh']
    proof = ddh_proof['proof']
    return ddh, proof


# Basic Crypto Layer Structures

def set_nirenc(ddh, proof):
    nirenc = set_ddh_proof(ddh, proof)
    return nirenc

def extract_nirenc(nirenc):
    ddh, proof = extract_ddh_proof(nirenc)
    return ddh, proof


# Transaction Layer Structures

def set_keys(ecc_key, nacl_key):
    return {
        'ecc': ecc_key,
        'nacl': nacl_key,
    }

def extract_keys(key):
    ecc_key  = key['ecc']
    nacl_key = key['nacl']
    return ecc_key, nacl_key

def set_proof(c_r, decryptor, nirenc, nidec):
    return {
        'c_r': c_r,
        'decryptor': decryptor, 
        'nirenc': nirenc, 
        'nidec': nidec,
    }

def extract_proof(proof):
    c_r = proof['c_r']
    decryptor = proof['decryptor']
    nirenc = proof['nirenc']
    nidec = proof['nidec']
    return c_r, decryptor, nirenc, nidec

