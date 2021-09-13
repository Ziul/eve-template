# Books' Schema
books_schema = {
    'name': {
        'type': 'string',
        'required': True
    },
    'cover': {'type': 'media', 'required': False},
    'owner': {
        'type': 'string',
        'nullable': False,
        'required': True,
        'data_relation': {
            'resource': 'user',
            'field': 'email',
            'embeddable': True
        }

    }

}

# Books settings
books = {
    'schema': books_schema,
    'allowed_roles': ['*'],
    'public_methods': ("GET", "HEAD"),
    'public_item_methods': ("GET", "HEAD"),
}