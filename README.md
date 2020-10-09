
# Installation

* Install poetry
* Clone this repository
* Run `poetry install`


# OpenID Configuration

Copy `copy.py.sample` to `copy.py` and edit it. 

## Important notes

Specify provider metadata is not supported yet, therefore your provider must support `/.well-known/openid-configuration` URL.

# Run app

```
poetry run flask run
```

