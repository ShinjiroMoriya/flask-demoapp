from app import app
from flask import render_template, url_for


class Error:

    def not_found():

        data = {
            'title': 'Not Found | Hello World',
        }

        return render_template('error/not_found.html', data=data), 404

    def server_error(error):

        data = {
            'title': 'Server Error | Hello World',
            'error': error
        }

        app.logger.error(error)

        return render_template('error/server_error.html', data=data), 500

    def database_error(error):

        app.logger.error(error)

        return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))
