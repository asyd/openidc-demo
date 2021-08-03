
# Installation

* Install poetry
* Clone this repository
* Run `poetry install`

# OpenID Configuration

Copy `config.py.sample` to `config.py` and edit it. 

## Keycloak configuration example

```python
openid_config = {
    'auto_discovery': True,
    'scope': ['openid', 'email', 'profile'],
    'client_id': 'test',
    'client_secret': 'ff57dbac-ac2d-4ea4-9158-4595e4a05c2c',
    'issuer': 'http://localhost:8080/auth/realms/<realm name>',
}
```

**The name of realm is case-sensitive!**

# Notes

Specify provider's metadata URL is not yet supported, therefore your provider must support `/.well-known/openid-configuration` URL.

# Run app

```
poetry run flask run --host $(hostname --fqdn)
```

