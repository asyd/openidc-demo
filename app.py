from flask import Flask, jsonify, render_template_string
from flask_pyoidc.provider_configuration import ProviderConfiguration, ClientMetadata, ProviderMetadata
from flask_pyoidc import OIDCAuthentication
from flask_pyoidc.user_session import UserSession
import logging
import flask
import socket
from config import openid_config
import sys
import string
import random

# auto import

logger = logging.getLogger(__name__)

# Perform initial checks on openid_conf
logging.basicConfig(
    level=logging.INFO,
)

provider_metadata = None

if 'auto_discovery' in openid_config.keys() and openid_config['auto_discovery']:
    openid_config['auto_discovery']
else:
    provider_metadata = ProviderMetadata(
        issuer=openid_config['issuer'],
        authorization_endpoint=openid_config['authorization_endpoint'],
        token_endpoint=openid_config['token_endpoint'],
    )

try:
    openid_config['scope']
except KeyError:
    openid_config['scope'] = ['openid', 'email', 'profile']

app = Flask(__name__)
app.config.update(
    SECRET_KEY=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16)),
    SERVER_NAME=f'{socket.getfqdn()}:5000',
    JSONIFY_PRETTYPRINT_REGULAR=True,
)

provider_config = ProviderConfiguration(
    auth_request_params={'scope': openid_config['scope']},
    issuer=openid_config['issuer'],
    provider_metadata=provider_metadata,
    client_metadata=ClientMetadata(
        client_id=openid_config['client_id'],
        client_secret=openid_config['client_secret'],
    )
)

auth = OIDCAuthentication({'default': provider_config}, app)


@app.route('/')
@auth.oidc_auth('default')
def login():
    user_session = UserSession(flask.session, provider_name='default')

    data = {
        'access_token': user_session.access_token,
        'id_token': user_session.id_token,
        'userinfo': user_session.userinfo,
    }
    return jsonify(data)


@app.route('/logout')
@auth.oidc_logout
def logout():
    return render_template_string(
        "<a href=\"{{ url_for('login') }}\">Login</a>"
    )
