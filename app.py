from flask import Flask, jsonify
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

logger = logging.getLogger(__name__)

# Perform initial checks on openid_conf
logging.basicConfig(
    level=logging.DEBUG,
)

try:
    openid_config['auto_discovery']
    if not openid_config['auto_discovery']:
        logger.critical("supplied metadata is not yet supported")
        sys.exit(1)
except KeyError:
    logger.critical('missing auto_discovery key')
    sys.exit(1)

try:
    openid_config['scope']
except KeyError:
    openid_config['scope'] = ['openid', 'email', 'profile']

app = Flask(__name__)
app.config.update(
    SECRET_KEY=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16)),
    SERVER_NAME=f'{socket.getfqdn()}:5000',
)

provider_config = ProviderConfiguration(
    auth_request_params={'scope': openid_config['scope']},
    issuer=openid_config['issuer'],
    client_metadata=ClientMetadata(
        client_id=openid_config['client_id'],
        client_secret=openid_config['client_secret'],
    )
)

auth = OIDCAuthentication({'default': provider_config}, app)


@app.route('/')
@auth.oidc_auth('default')
def login():
    user_session = UserSession(flask.session, provider_name='default').userinfo
    print(user_session)
    return jsonify(user_session)


@app.route('/logout')
@auth.oidc_logout
def logout():
    return 'logged out'
