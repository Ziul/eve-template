from flask_bcrypt import generate_password_hash


def create_password(password):
    """
    Encodes password
    """
    return generate_password_hash(password.encode()).decode()


# User Schema
user_schema = {
    'email': {
        'type': 'string',
        'required': True,
        'regex': r"(^[a-z0-9_.+-]+@[a-z0-9-]+\.[a-z0-9-.]+$)"
    },
    'password': {
        'type': 'string',
        'required': True, 'empty': False,
        'nullable': False, 'coerce': (str, create_password)
    },
    'name': {
        'type': 'string',
        'required': True
    },
    'picture': {'type': 'media', 'required': False},
}

# User settings
user = {
    'schema': user_schema,
    'public_methods': ("POST", "HEAD"),
    'mongo_indexes': {
        'id': (
            [
                ('email', 1)
            ],
            {'unique': True}
        ),
        'query': (
            [
                ('name', 'text'),
                ('email', 'text'),
            ],
            {
                'default_language': 'portuguese',
                'background': True
            }
        )
    },
    'datasource': {
        'source': 'user',
        'projection': {  # campos para serem omitidos
            'password': 0,
        },
    },

}