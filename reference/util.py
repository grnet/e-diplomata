# Structures

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

def set_proof(u_comm, v_comm, s, d):
    return {
        'u_comm': u_comm,
        'v_comm': v_comm,
        's': s,
        'd': d,
    }

def extract_proof(proof):
    u_comm = proof['u_comm']
    v_comm = proof['v_comm']
    s = proof['s']
    d = proof['d']
    return u_comm, v_comm, s, d

def set_ddh_proof(ddh, proof):
    return {
        'ddh': ddh,
        'proof': proof
    }

def extract_ddh_proof(ddh_proof):
    ddh = ddh_proof['ddh']
    proof = ddh_proof['proof']
    return ddh, proof

def set_nirenc(proof_c1, proof_c2):
    return {
        'proof_c1': proof_c1,
        'proof_c2': proof_c2,
    }

def extract_nirenc(nirenc):
    proof_c1 = nirenc['proof_c1']
    proof_c2 = nirenc['proof_c2']
    return proof_c1, proof_c2

