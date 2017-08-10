from app import app
from jinja2 import Environment, FileSystemLoader, Markup

from flask_htmlmin import HTMLMIN

# Minify
HTMLMIN(app)

# Jinja Loader
app.jinja_loader = FileSystemLoader('app/static/views')
