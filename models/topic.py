from config import *
import uuid


class Topic(db.Model):
    """
    トピックモデル
    """
    __tablename__ = "topics"

    topicid = db.Column(
        db.Integer,
        primary_key=True
    )
    topic_delete = db.Column(
        db.Boolean,
    )
    topicuuid = db.Column(
        db.String(255),
    )
    userid = db.Column(
        db.Integer,
        db.ForeignKey('users.userid')
    )
    topic = db.Column(
        db.UnicodeText
    )
    topic_markdown = db.Column(
        db.UnicodeText
    )
    image = db.Column(
        db.String(255),
    )
    image_id = db.Column(
        db.String(255),
    )
    created = db.Column(
        db.String(255),
    )
    modified = db.Column(
        db.String(255),
    )
    # ユーザーとのリレーションを作成
    user = relationship('User', backref=backref('topics'))

    # 初期化
    def __init__(self, userid=None, topic=None, topic_markdown=None, image=None, image_id=None):
        self.topic_delete = False
        self.topicuuid = uuid.uuid4()
        self.userid = userid
        self.topic = topic
        self.topic_markdown = topic_markdown
        self.image = image
        self.image_id = image_id
        self.created = datetime.now(tz=jptime()).strftime('%Y-%m-%d %H:%M:%S')
        self.modified = datetime.now(tz=jptime()).strftime('%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        return '<Topics %r>' % self.topicid
