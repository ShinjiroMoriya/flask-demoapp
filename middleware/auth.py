from functools import wraps
from config import *
from flask import request, Response, redirect, url_for, g
from models.user import User


def required(func):

    @wraps(func)
    def decorated_view(*args, **kwargs):

        userid = session.get('userid')

        if userid is None:

            g.user = None

            return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

        else:

            try:

                user = User.query.filter_by(userid=userid).first()
                g.user = {
                    'userid': user.userid,
                    'name': user.name,
                    'email': user.email,
                    'icon': user.icon
                }

            except Exception as e:

                app.logger.error(e)

                g.user = None

                return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

        return func(*args, **kwargs)

    return decorated_view


def check_auth(username, password):
    return username == app.config.get('AUTH_ID') and password == app.config.get('AUTH_PASSWORD')

# Before Request Function


@app.before_request
def requires_auth():
    if app.config.get('AUTH'):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return Response(
                'Authorization Required</h1>', 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            )
