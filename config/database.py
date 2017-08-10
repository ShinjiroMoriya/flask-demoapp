from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref

# db = Database()
db = SQLAlchemy(app)

# Database Create


@app.before_first_request
def init():
    db.create_all()
