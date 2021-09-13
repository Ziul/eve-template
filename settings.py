from os import environ
from uuid import uuid4
from eve_swagger import get_swagger_blueprint, add_documentation
from eve.io.mongo import GridFSMediaStorage
from models import DOMAIN

try:
    from dotenv import load_dotenv, find_dotenv
    # try to load.env files
    load_dotenv(find_dotenv())
except EnvironmentError as env_error:
    pass

# App Settings
APP_VERSION = '1.0.0'

# Mongo config
MONGO_URI = environ.get("MONGO_HOST", environ.get("MONGO_URI", 'localhost'))
MONGO_DBNAME = environ.get("MONGO_DBNAME", 'example')
PORT = environ.get("PORT", 5000)
SECRET_KEY = uuid4().hex
DEBUG = bool(int(environ.get("DEBUG", 0)))
TESTING = bool(int(environ.get("DEBUG", 0)))
OPLOG=bool(int(environ.get("OPLOG", 1)))
OPLOG_AUDIT=bool(int(environ.get("OPLOG", 1)))
OPLOG_ENDPOINT='oplog'
SCHEMA_ENDPOINT = 'schema'
# INFO = '_info'

# Cookies
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# Eve settings
RENDERERS = ['eve.render.JSONRenderer']
# X_DOMAINS = ['*']
# X_HEADERS = ['*']
# X_EXPOSE_HEADERS = ['*']
# URL_PREFIX = 'v1'
# MONGO_QUERY_BLACKLIST = ['$where']
# PAGINATION_LIMIT = 600
# SEND_FILE_MAX_AGE_DEFAULT = 0

#  Eve Media
RETURN_MEDIA_AS_BASE64_STRING = False
RETURN_MEDIA_AS_URL = True
EXTENDED_MEDIA_INFO = ['content_type', 'filename', 'length', 'md5', 'uploadDate']

# Eve Features
AUTO_CREATE_LISTS = True
IF_MATCH = False
# SOFT_DELETE = True

# Eve methods
RESOURCE_METHODS = ['GET', 'POST']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

# Media Storage
MEDIA_ENDPOINT = 'media'
MEDIA_STORAGE = GridFSMediaStorage

# JWT settings
JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY", 'YourSecretPassword')
JWT_ALGORITHM = environ.get("JWT_ALGORITHM", 'HS256')
JWT_DECODE_ALGORITHMS = [JWT_ALGORITHM]

# Swagger
SWAGGER_INFO = {
    'title': "Eve Example API",
    'version': APP_VERSION,
    'description': 'Just to have a more complete example',
    'contact': {
        'name': 'Luiz Oliveira',
        'email': 'ziuloliveira@gmail.com'
    },
    'schemes': ['http']
}
ENABLE_HOOK_DESCRIPTION = True
swagger = get_swagger_blueprint()
SERVERS_URL = {
    'servers': [
        {'url': 'http://127.0.0.1:5000'},
    ]
}
add_documentation(swagger, SERVERS_URL)
