# Protocol

```commandline
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

```commandline
python3 demo.py
```

## Key management

### Keys

<br>*Non-serialized*

```
{
    'ecc': <Cryptodome.PublicKey.ECC.EccKey>
    'nacl': <nacl.public.PrivateKey>
}
```

<br>*Serialized*

```
{
    'ecc': {
        'x': <int>
        'y': <int>
        'd': <int>
    },
    'nacl': <str(hex)>
}
```

### Public shares

<br>*Non-serialized*

```
{
    'ecc': <Cryptodome.PublicKey.ECC.EccPoint>,
    'nacl': <nacl.public.PublicKey>
}
```

<br>*Serialized*
```
{
    'ecc': [<int>, <int>],
    'nacl': <str(hex)>
}
```

### JSON I/O

#### `Issuer.publish_award()`

<br>*input*
```
t: <bytes>
```

<br>*output*
```
s_awd <str(hex)>

c {
    c1: [<int>, <int>],
    c2: [<int>, <int>]
}

r <int>
```

#### `Holder.publish_request()`

<br>*input*
```
s_awd <str>

verifier_pub {
    ecc: [<int>, <int>],
    nacl: <str(hex)>
}
```

<br>*output*
```
s_req <str(hex)>
```

#### `Issuer.publish_proof()`

<br>*input*
```
s_req <str(hex)>

r <int>

c {
    c1: [<int>, <int>],
    c2: [<int>, <int>]
}

verifier_pub {
    ecc: [<int>, <int>],
    nacl: <str(hex)>
}
```

<br>*output*
```
s_prf <str(hex)>

proof {
    c_r: {
        c1: [<int>, <int>],
        c2: [<int>, <int>]
    },
    decryptor: <str(hex)>,
    nirenc: {
        proof_c1: {
            ddh: [
                [<int>, <int>],
                [<int>, <int>],
                [<int>, <int>]
            ],
            proof: {
                  u_comm: [<int>, <int>],
                  v_comm: [<int>, <int>],
                  s: <int>,
                  d: [<int>, <int>],
            }
        },
        proof_c2: {
            ddh: [
                [<int>, <int>],
                [<int>, <int>],
                [<int>, <int>]
            ],
            proof: {
                  u_comm: [<int>, <int>],
                  v_comm: [<int>, <int>],
                  s: <int>,
                  d: [<int>, <int>],
            }
        },
    },
    niddh: <str(hex)>
}
```

#### `Verifier.publish_ack()`

<br>*input*

```
s_prf <str(hex)>

t <bytes>

proof {
  ...
}

issuer_pub {
    ecc: [<int>, <int>],
    nacl: <str(hex)>
}
```

<br>*output*
```
s_ack <str(hex)>

result <bool>
```


## Dev

```commandline
pip install -r requirements-dev.txt
python3 -m pytest test.py
```
