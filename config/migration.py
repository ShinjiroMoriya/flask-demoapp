from app import app

from config.database import db

from flask_migrate import Migrate

migrate = Migrate(app, db)
