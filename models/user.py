from config import *
import uuid


class User(db.Model):
    """
    ユーザーモデル
    """
    __tablename__ = "users"

    userid = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(255),
    )
    email = db.Column(
        db.String(255),
    )
    password = db.Column(
        db.String(255),
    )
    token = db.Column(
        db.String(255),
    )
    valid = db.Column(
        db.Boolean,
    )
    google_id = db.Column(
        db.String(255),
    )
    twitter_id = db.Column(
        db.String(255),
    )
    facebook_id = db.Column(
        db.String(255),
    )
    github_id = db.Column(
        db.String(255),
    )
    temporary = db.Column(
        db.String(255),
    )
    icon = db.Column(
        db.String(255),
    )
    icon_id = db.Column(
        db.String(255),
    )
    created = db.Column(
        db.String(255),
    )
    modified = db.Column(
        db.String(255),
    )

    # 初期化
    def __init__(
            self,
            name=None,
            email=None,
            password=None,
            valid=False,
            google_id=None,
            twitter_id=None,
            facebook_id=None,
            github_id=None,
            temporary=None,
            icon_id=None):

        self.name = name
        self.email = email
        self.set_password(password)
        self.token = uuid.uuid4()
        self.valid = valid
        self.google_id = google_id
        self.twitter_id = twitter_id
        self.facebook_id = facebook_id
        self.github_id = github_id
        self.temporary = temporary
        self.icon = '/assets/img/icon.jpg'
        self.icon_id = icon_id
        self.created = datetime.now(tz=jptime()).strftime('%Y-%m-%d %H:%M:%S')
        self.modified = datetime.now(tz=jptime()).strftime('%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        return '<Users %r>' % self.name

    def set_password(self, password):
        if password:
            self.password = bcrypt.generate_password_hash(password)
        else:
            self.password = None
