from app import app

from flask_bcrypt import Bcrypt

# Hash化
bcrypt = Bcrypt(app)
