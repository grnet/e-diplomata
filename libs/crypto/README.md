# Diplomata

Python reference implementation of the DIPLOMATA protocol

## Overview

## Demo

```commandline
python3 demo.py [--help]
```
```
usage: python3 demo.py [OPTIONS]

Diplomata Demo Script

optional arguments:
  -h, --help     show this help message and exit
  --curve CURVE  Elliptic curve of El-Gamal cryptosystem (default: P-384)
  --title TITLE  Content of title under verification (default: "This is a qualification")
  --hexify       Hexify big integers at serialization (default: False)
  --flatten      Flatten serialized objects (default: False)
  --verbose      Display computation results at each step (default: False)
```

## Usage

```python
from diplomata.protocol import KeyManager, Holder, Issuer, Verifier

title = "This is a qualification"

# Setup

config = {
    'curve': 'P-384',
    'hexifier': True,
    'flattener': False
}

km = KeyManager(**config)

holder_key = km.generate_keys()
issuer_key = km.generate_keys()
verifier_key = km.generate_keys()

holder = Holder.from_key(holder_key, **config)
issuer = Issuer.from_key(issuer_key, **config)
verifier = Verifier.from_key(verifier_key, **config)

holder_pub = holder.get_public()
issuer_pub = issuer.get_public()
verifier_pub = verifier.get_public()


# Run protocol

s_awd, c, r = issuer.publish_award(title)                               # step 1
s_req = holder.publish_request(s_awd, verifier_pub)                     # step 2
s_prf, proof = issuer.publish_proof(s_req, r, c, verifier_pub)          # step 3
s_ack, result = verifier.publish_ack(s_prf, title, proof, issuer_pub)   # step 4

assert result
```

## API (TODO)

Refer to [TYPES.md](./TYPES.md) for a specification of the JSON structures
appearing in the presentation layer.

### `KeyManager`

#### .generate_keys()
#### .get_public_shares()

### `Party`

#### .from_key()
#### .get_public()
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

## Dev

### Tests

```commandline
pip install -r requirements-dev.txt
./test.sh [...]
```
