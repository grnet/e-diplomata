# Diplomata protocol lib

## Overview

### Elgamal backend info

## Demo

```commandline
python3 demo.py
```

## Usage

```python
from protocol import KeyGenerator, Holder, Issuer, Verifier

CURVE = 'P-384'

# Generate keys

kg = KeyGenerator(CURVE)
holder_key = kg.generate_keys()
issuer_key = kg.generate_keys()
verifier_key = kg.generate_keys()

# Setup involved parties

holder = Holder.create_from_key(curve=CURVE, key=holder_key)
issuer = Issuer.create_from_key(curve=CURVE, key=issuer_key)
verifier = Verifier.create_from_key(curve=CURVE, key=verifier_key)

t = "This is a qualification".encode('utf-8')

# Protocol execution

s_awd, c, r = issuer.publish_award(t)                               # step 1
s_req = holder.publish_request(s_awd, verifier_pub)                 # step 2
s_prf, proof = issuer.publish_proof(s_req, r, c, verifier_pub)      # step 3
s_ack, result = verifier.publish_ack(s_prf, t, proof, issuer_pub)   # step 4
```

## API

### Types

```
key {
    ecc: {
        x: <int>,
        y: <int>,
        d: <int>
    },
    nacl: <str(hex)>
}
```

```
pub {
    ecc: [<int>, <int>],
    nacl: <str(hex)>
}
```

```
comm {
    c1: [<int>, <int>],
    c2: [<int>, <int>]
}
```

```
ddh [
    [<int>, <int>], 
    [<int>, <int>], 
    [<int>, <int>]
]
```

```
chaum-pedersen {
    u_comm: [<int>, <int>],
    v_comm: [<int>, <int>],
    s: <int>,
    d: [<int>, <int>]
}
```

```
ddh-proof {
    ddh: <ddh>.
    proof: <chaum-pedersen>
}
```

```
proof {
    c_r: {
        c1: [<int>, <int>],
        c2: [<int>, <int>]
    },
    decryptor: <str(hex)>,
    nirenc: {
        proof_c1: <ddh-proof>,
        proof_c2: <ddh-proof>
    },
    niddh: <str(hex)>
}
```

### Functions

```
Issuer.publish_award(t: <bytes>) -> (s_awd: <str(hex)>, c: <comm>, r: <int>)
Holder.publish_request(s_awd: <str(hex)>, verifier_pub: <pub>) -> s_req: <str(hex)>
Issuer.publish_proof(s_req: <str(hex)>, r: <int>, c: <comm>, verifier_pub: <pub>) -> (s_prf: <str(hex)>, proof: <proof>)
Verifier.publish_ack(s_prf: <str(hex)>, t: <bytes>, proof: <proof>, issuer_pub: <pub>) -> (s_ack: <str(hex)>, result: <bool>)
```

## Dev

### Tests

```commandline
pip install -r requirements-dev.txt
python3 -m pytest test.py
```
