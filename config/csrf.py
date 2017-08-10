from app import app

from flask_wtf.csrf import CsrfProtect
from flask import render_template

# CSRF
csrf = CsrfProtect()
csrf.init_app(app)

# CSRF Error Handler


@csrf.error_handler
def csrf_error(reason):

    data = {
        'title': 'Error | Hello World',
        'reason': reason,
    }

    return render_template('error/csrf_error.html', data=data), 400
