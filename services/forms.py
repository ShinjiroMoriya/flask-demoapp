from wtforms import Form, StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(Form):

    email = EmailField(
        'email',
        validators=[
            DataRequired(),
            Email(),
            Length(max=255),
        ]
    )
    password = PasswordField(
        'password',
        validators=[
            DataRequired(),
            Length(max=255),
        ]
    )


class RegisterForm(Form):

    name = StringField(
        'name',
        validators=[
            DataRequired(),
            Length(max=255),
        ]
    )
    email = EmailField(
        'email',
        validators=[
            DataRequired(),
            Email(),
            Length(max=255),
        ]
    )
    password = PasswordField(
        'password',
        validators=[
            DataRequired(),
            Length(max=255),
        ]
    )


class RegisterSocialForm(Form):

    name = StringField(
        'name',
        validators=[
            DataRequired(),
            Length(max=255),
        ]
    )
    email = EmailField(
        'email',
        validators=[
            DataRequired(),
            Email(),
            Length(max=255),
        ]
    )


class UpdateNameForm(Form):

    name = StringField(
        'name',
        validators=[
            DataRequired(),
            Length(max=255),
        ]
    )


class EmailForm(Form):

    email = StringField(
        'email',
        validators=[
            DataRequired(),
            Length(max=255),
        ]
    )


class PasswordForm(Form):

    password = PasswordField(
        'password',
        validators=[
            DataRequired(),
            Length(max=255),
        ]
    )


class PasswordRemindForm(Form):

    password = PasswordField(
        'password',
        validators=[
            DataRequired(),
            Length(max=255),
        ]
    )
    token = StringField(
        'token',
        validators=[
            DataRequired(),
            Length(max=255),
        ]
    )


class TopicForm(Form):

    topic = TextAreaField(
        'topic',
        validators=[
            DataRequired(),
            Length(max=4000000),
        ]
    )


class CommentForm(Form):

    comment = TextAreaField(
        'comment',
        validators=[
            DataRequired(),
            Length(max=4000000),
        ]
    )


def file_ext_check(ext, type='image'):

    ext = ext.lower()

    if type == 'image':
        for var in ['.jpg', '.jpeg', '.png', '.gif']:
            if ext == var:
                return

    return True


def error_message(form):

    if 'name' in form:

        return '名前を入力してください'

    if 'email' in form:

        return 'Emailアドレスを入力してください'

    if 'password' in form:

        return 'パスワードを入力してください'

    if 'topic' in form:

        return '内容を入力してください'

    if 'comment' in form:

        return 'コメントを入力してください'
