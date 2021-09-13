from os import environ
JWT_ACCESS_TOKEN_EXPIRES = int(environ.get("JWT_ACCESS_TOKEN_EXPIRES", 24*60*60*1))  # 24h

# Token Schema
tokens_schema = {
    "token": {
        'type': 'string',
        'required': True
    },
    'username': {
        'type': 'string',
        'required': True
    },
    'role': {
        'type': 'string',
        'required': False,
        'default': 'user',
        'allowed': [
            'user',
            'admin',
            'sudo'
        ]
    },
    'iat': {  # Issued At Time
        'type': 'integer',
        'required': True
    },
    'nbf': {  # Not Before
        'type': 'integer',
        'required': True
    },
    'jti': {  # JWT ID
        'type': 'string',
        'required': True
    },
    'exp': {  # Expiration Time
        'type': 'integer',
        'required': True
    },
    'fresh': {
        'type': 'string',
        'required': True
    },
    'type': {
        'type': 'string',
        'required': True
    },
    'identity': {
        'type': 'string',
        'required': False
    },
}

# Token settings
token = {
    'schema': tokens_schema,
    'item_title': 'Token',
    'allowed_roles': ['admin', 'sudo'],
    'disable_documentation': True,
    'internal_resource': True,
    'datasource': {
        'source': 'tokens',
    },
    'mongo_indexes': {
        'exp': (
            [
                ('exp', 1)
            ],
            {'expireAfterSeconds': JWT_ACCESS_TOKEN_EXPIRES}
        ),
        'token': (
            [
                ('token', 1),
                ('username', 1)
            ]
        )
    }
}
