import os
from app import app

app.config['AUTH'] = os.environ.get('AUTH')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['MINIFY_PAGE'] = True
app.config['SESSION_COOKIE_NAME'] = 'Hello World'
app.config['SESSION_TYPE'] = 'redis'
app.config['SQLALCHEMY_POOL_SIZE'] = 5
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 10
app.config['PERMANENT_SESSION_LIFETIME'] = 60 * 24 * 1  # 60（1時間） * 24（1日） * 7日
app.config['MAX_CONTENT_LENGTH'] = 5242880
app.config['SECRET_KEY'] = os.urandom(24)
app.config['REDIS_URL'] = os.environ.get('REDIS_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['URL'] = os.environ.get('SITE_URL')
app.config['SENDGRID_API_KEY'] = os.environ.get('SENDGRID_API_KEY')
app.config['SENDGRID_PASSWORD'] = os.environ.get('SENDGRID_PASSWORD')
app.config['SENDGRID_USERNAME'] = os.environ.get('SENDGRID_USERNAME')
app.config['GOOGLE_ID'] = os.environ.get('GOOGLE_ID')
app.config['GOOGLE_SECRET'] = os.environ.get('GOOGLE_SECRET')
app.config['TWITTER_KEY'] = os.environ.get('TWITTER_KEY')
app.config['TWITTER_SECRET'] = os.environ.get('TWITTER_SECRET')
app.config['FACEBOOK_APP_ID'] = os.environ.get('FACEBOOK_APP_ID')
app.config['FACEBOOK_APP_SECRET'] = os.environ.get('FACEBOOK_APP_SECRET')
app.config['GITHUB_KEY'] = os.environ.get('GITHUB_KEY')
app.config['GITHUB_SECRET'] = os.environ.get('GITHUB_SECRET')
app.config['FROM_EMAIL'] = os.environ.get('FROM_EMAIL')
app.config['AUTH_ID'] = os.environ.get('AUTH_ID')
app.config['AUTH_PASSWORD'] = os.environ.get('AUTH_PASSWORD')
app.config['POST_PER_PAGE'] = os.environ.get('POST_PER_PAGE')
app.config['SCHEME'] = os.environ.get('SCHEME', 'http')
