from eve import Eve
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter
from flask import jsonify, session, request
from flask import jsonify
from flask_jwt_extended import JWTManager
from auth import JWTAuth, auth
import settings
from flask_cors import CORS
from flask_compress import Compress

if settings.USE_AUTH:
    app = Eve('api', auth=JWTAuth, media=settings.MEDIA_STORAGE)
else:
    app = Eve('api', media=settings.MEDIA_STORAGE)

CORS(app)
Compress(app)


# DEBUG must be off or DEBUG_METRICS on
metrics = PrometheusMetrics(
    app,
    group_by='url_rule',
    excluded_paths=['/favicon.ico'],
    defaults_prefix='#no_prefix',
    default_labels={
        'isError': lambda r: r.status_code>=400,
        'type': lambda: request.scheme,
        'addr': lambda: request.url_rule if request.url_rule!= None else '/' + request.path.split('/')[1] + '/<param>'
    }
)

metrics.info(
    'application_info',
    "records static application info such as it's semantic version number", 
    version=app.config['APP_VERSION'],
    app=app.name
)

metrics_request_size =  Counter(
        "response_size_bytes",
        "counts the size of each http response",
        ["type", "status", "isError", "method", "addr"],
        registry=metrics.registry
    )

app.register_blueprint(settings.swagger)
app.register_blueprint(auth)
__jwt_manager__ = JWTManager(app)

@__jwt_manager__.user_claims_loader
def add_claims_to_access_token(user):
    """
    Create a function that will be called whenever create_access_token
    is used. It will take whatever object is passed into the
    create_access_token method, and lets us define what custom claims
    should be added to the access token.
    """
    return {'role': user.role, 'session': session.get('data')}

@__jwt_manager__.user_identity_loader
def user_identity_lookup(user):
    """
    Create a function that will be called whenever create_access_token
    is used. It will take whatever object is passed into the
    create_access_token method, and lets us define what the identity
    of the access token should be.
    """
    return user.user_id

@app.route('/favicon.ico', methods=['GET'])
def favicon():
    """
    Just a positive favicon
    """
    return jsonify(status='OK'), 200

def after_request(response):
    metrics_request_size.labels(
        request.scheme,
        response.status_code,
        response.status_code>=400,
        request.method,
        request.url_rule if request.url_rule!= None else '/' + request.path.split('/')[1] + '/<param>',
    ).inc(int(response.headers.get("Content-Length", 0)))
    return response

app.after_request(after_request)


if __name__ == '__main__':
    app.run(debug=settings.DEBUG, host='0.0.0.0', port=settings.PORT)
