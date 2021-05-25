# Diplomata protocol lib

## Overview

## Demo

```commandline
python3 demo.py
```

## Usage

```python
from diplomata.protocol import KeyManager, Holder, Issuer, Verifier

CURVE = 'P-384'


# Generate keys

km = KeyManager(CURVE)
holder_key = km.generate_keys()
issuer_key = km.generate_keys()
verifier_key = km.generate_keys()


# Setup involved parties

holder = Holder.create_from_key(curve=CURVE, key=holder_key)
issuer = Issuer.create_from_key(curve=CURVE, key=issuer_key)
verifier = Verifier.create_from_key(curve=CURVE, key=verifier_key)


# Involved parties publish their keys

holder_pub = holder.get_public_shares()
issuer_pub = issuer.get_public_shares()
verifier_pub = verifier.get_public_shares()


# Run protocol

title = "This is a qualification".encode('utf-8')

s_awd, c, r = issuer.publish_award(title)                               # step 1
s_req = holder.publish_request(s_awd, verifier_pub)                     # step 2
s_prf, proof = issuer.publish_proof(s_req, r, c, verifier_pub)          # step 3
s_ack, result = verifier.publish_ack(s_prf, title, proof, issuer_pub)   # step 4
```

## API (TODO)

Refer to [TYPES.md](./TYPES.md) for a specification of the JSON structures
appearing in the presentation layer.

### `KeyManager`

#### KeyManager(*curve='P-384'*)
#### .generate_keys()

### `Party`

#### .create_from_key()
#### .get_public_shares()
#### .sign()
#### .verify_signature()
#### .encrypt()
#### .decrypt()

### `Holder`

#### Holder.publish_request()

### `Issuer`

#### Issuer.publish_award()
#### Issuer.publish_proof()

### `Verifier`

#### Verifier.publish_ack()

<!--
```
Issuer.publish_award(t: <bytes>) -> (s_awd: <str(hex)>, c: <comm>, r: <int>)
Holder.publish_request(s_awd: <str(hex)>, verifier_pub: <pub>) -> s_req: <str(hex)>
Issuer.publish_proof(s_req: <str(hex)>, r: <int>, c: <comm>, verifier_pub: <pub>) -> (s_prf: <str(hex)>, proof: <proof>)
Verifier.publish_ack(s_prf: <str(hex)>, t: <bytes>, proof: <proof>, issuer_pub: <pub>) -> (s_ack: <str(hex)>, result: <bool>)
```
-->

## Dev

### Tests

```commandline
pip install -r requirements-dev.txt
./test.sh [...]
```
