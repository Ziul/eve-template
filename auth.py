import traceback
from datetime import datetime
import jwt
from eve.utils import config
from eve.auth import TokenAuth
from flask_jwt_extended import create_access_token
from flask  import current_app as app
from flask import request, jsonify, Blueprint, abort
from flask_bcrypt import check_password_hash
from bson import ObjectId
from eve_swagger import add_documentation
import settings



class JWTAuth(TokenAuth):
    """ Module to validate the auth user to access the API data"""
    exception = "Please provide proper credentials"

    def authenticate(self):
        """ Returns a standard a 401 response that enables basic auth.
        Override if you want to change the response and/or the realm.
        """
        abort(
            401,
            description=self.exception,
            www_authenticate=("WWW-Authenticate", 'Basic realm="%s"' % __package__),
            )

    def authorized(self, allowed_roles, resource, method):
        super().authorized( allowed_roles, resource, method)

    def check_auth(self, token, allowed_roles, resource, method):
        """
        Validate token
        """
        payload = {}
        try:
            payload = jwt.decode(
                token,
                app.config['JWT_SECRET_KEY'],
                algorithms=app.config['JWT_DECODE_ALGORITHMS'])
        except jwt.exceptions.ExpiredSignatureError:
            traceback.print_exc()
            self.exception = 'Token expired'
            return False
        except Exception as ex:
            traceback.print_exc()
            self.exception = "Invalid Credentials. %s" % str(ex)
            return False

        role = payload.get('user_claims', {}).get('role')
        if allowed_roles:
            if role not in allowed_roles or '*' not in allowed_roles :
                self.exception = "Role from user %s not allowed" % payload.get(
                    'identity')
                return False
        # Check if User stills in database
        users = app.data.driver.db[config.DOMAIN['user']['datasource']['source']]
        user_documment = users.find_one({'_id': ObjectId(payload.get('identity'))})
        if not user_documment:
            self.exception = 'User not found'
            return False
        if app.config.get('KEEP_TOKEN'):
            # Check if token stillin the database
            tokens = app.data.driver.db[config.DOMAIN['token']['datasource']['source']]
            # if token still in db, return true
            token_document = tokens.find_one({'token': token})
            if not bool(token_document):
                app.logger.warning('Token for %s not in db anymore', payload.get('identity'))
                self.exception = "Invalid Credentials. Invalid Token"
                return False
        self.set_user_or_token(ObjectId(payload.get('identity')))
        self.set_request_auth_value(ObjectId(payload.get('identity')))
        return bool(user_documment)

auth = Blueprint('auth', __name__, template_folder='auth', url_prefix='/auth')

class User():
    """
    Basic user to insert some claims
    """
    def __init__(self, user_id, username, role):
        self.user_id = user_id
        self.username = username
        self.role = role

def create_token(user):
    """
    Creates a token based on a user
    """
    access_token = create_access_token(user)
    payload = jwt.decode(
        access_token,
        app.config['JWT_SECRET_KEY'],
        algorithms=app.config['JWT_DECODE_ALGORITHMS'])
    data = {
        'token':access_token,
        'username': user.username,
    }
    data.update(payload)
    data['exp'] = datetime.fromtimestamp(data['exp'])
    app.logger.debug(str(data))
    if app.config.get('KEEP_TOKEN'):
        # deletes old tokens
        tokens = app.data.driver.db[config.DOMAIN['token']['datasource']['source']]
        tokens.delete_many({'username': user.username})
        # insets new token
        result = app.data.insert('token', data)
        return access_token, str(result[0])

    return access_token, None

@auth.route('/token', methods=['POST'])
def get_token():
    """
    Generate a valid token
    """
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username:
        abort(400, "Invalid username or password")
    if not password:
        abort(400, "Invalid username or password")
    users = app.data.driver.db[config.DOMAIN['user']['datasource']['source']]
    user = users.find_one({'email':username})
    # validate the user in the user's service
    if not user:
        abort(401, "Invalid username or password")
    if not check_password_hash(user.get('password'), password):
        abort(401, "Invalid username or password")
    role = user.get('role', 'user')
    user_id = str(user.get('_id'))
    user = User(user_id, username, role)
    access_token, refresh_token = create_token(user)
    return jsonify(
        token=access_token,
        type='bearer',
        roles=role,
        user=username,
        refreshToken=refresh_token), 200


add_documentation(settings.swagger, {
    'paths': {
        '/auth/token': {
            'post': {
                'requestBody': {
                    'description': 'Authenticate and creates a token for a user',
                    'required': True,
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'required': ['username', 'password'],
                                'properties': {
                                    'username': {
                                        'type': 'string',
                                        'description': "User's Email",
                                        'example': 'user@mail.com',
                                    },
                                    'password': {
                                        'type': 'string',
                                        'description': "User's Password",
                                        'example': 'newAndStrongPassword',
                                    }
                                }
                            }
                        }
                    },
                },
                'summary': 'Authenticate and creates a token for a user',
                'responses': {
                    '200': {'description': 'Token generated'},
                    '400': {'description': 'Bad Request'},
                    '401': {'description': 'Wrong password or user not found'},
                },
                'tags': ['Auth']
            }
        }
    }
})
