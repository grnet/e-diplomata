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
    'nacl': <str> (hexadecimal)
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
    'nacl': <str> (hexadecimal)
}
```

## Dev

```commandline
pip install -r requirements-dev.txt
python3 -m pytest test.py
```
