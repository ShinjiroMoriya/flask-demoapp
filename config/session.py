from app import app
from flask import session
from flask_session import Session
from flask_redis import FlaskRedis

app.config['SESSION_REDIS'] = FlaskRedis(app)

Session(app)
