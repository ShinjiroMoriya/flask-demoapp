from config import *
import uuid


class Comment(db.Model):
    """
    コメントモデル
    """
    __tablename__ = "comments"

    commentid = db.Column(
        db.Integer,
        primary_key=True
    )
    commentuuid = db.Column(
        db.String(255),
    )
    topicid = db.Column(
        db.Integer,
        db.ForeignKey('topics.topicid')
    )
    userid = db.Column(
        db.Integer,
        db.ForeignKey('users.userid')
    )
    comment_delete = db.Column(
        db.Boolean,
    )
    comment = db.Column(
        db.UnicodeText
    )
    comment_markdown = db.Column(
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
    # ユーザー、トピックとのリレーションを作成
    user = relationship('User', backref=backref('comments'))
    topic = relationship('Topic', backref=backref('comments'))

    # 初期化
    def __init__(self, topicid=None, userid=None, comment=None, comment_markdown=None, image=None, image_id=None):
        self.comment_delete = False
        self.commentuuid = uuid.uuid4()
        self.topicid = topicid
        self.userid = userid
        self.comment = comment
        self.comment_markdown = comment_markdown
        self.image = image
        self.image_id = image_id
        self.created = datetime.now(tz=jptime()).strftime('%Y-%m-%d %H:%M:%S')
        self.modified = datetime.now(tz=jptime()).strftime('%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        return '<Comments %r>' % self.userid
