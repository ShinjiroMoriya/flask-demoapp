from app import socketio, emit
from config import *
from controllers import *
from middleware import auth
from sqlalchemy.exc import SQLAlchemyError

# Top
app.add_url_rule(
    '/',
    view_func=Index.as_view('index'))


# Valid
app.add_url_rule(
    '/valid',
    view_func=IndexValid.as_view('index_valid'))


# Email Valid
app.add_url_rule(
    '/email',
    view_func=IndexMailValid.as_view('index_email_valid'))


# Send
app.add_url_rule(
    '/send',
    view_func=IndexSend.as_view('send'))


# Forgut Password
app.add_url_rule(
    '/password',
    view_func=IndexPassword.as_view('index_password'))


# Forgut Password Send
app.add_url_rule(
    '/password/remind',
    view_func=IndexPasswordRemind.as_view('index_password_remind'))


# Forgut Password Change
app.add_url_rule(
    '/password/change',
    view_func=IndexPasswordChange.as_view('index_password_change'))


# Forgut Password Change Post
app.add_url_rule(
    '/password/change/post',
    view_func=IndexPasswordChangePost.as_view('index_password_change_post'))


# Regsiter
app.add_url_rule(
    '/register',
    view_func=RegisterIndex.as_view('register'))


# Regsiter Create
app.add_url_rule(
    '/register/create',
    view_func=RegisterCreate.as_view('register_create'))


# Social Login Social Register
app.add_url_rule(
    '/social/register',
    view_func=RegisterSocial.as_view('register_social'))


# Social Login Social Register Create
app.add_url_rule(
    '/social/register/create',
    view_func=RegisterSocialCreate.as_view('register_social_create'))


# Topics Top
app.add_url_rule(
    '/topics',
    view_func=TopicsIndex.as_view('topics_index'))


# Topics Detail
app.add_url_rule(
    '/topics/<uuid>',
    view_func=TopicsDetail.as_view('topics_detail'))


# Mypage Top
app.add_url_rule(
    '/mypage',
    view_func=auth.required(MypageIndex.as_view('mypage_index')))


# Mypage Account
app.add_url_rule(
    '/mypage/account',
    view_func=auth.required(MypageAccount.as_view('mypage_account')))


# Mypage Account Name
app.add_url_rule(
    '/mypage/account/name',
    view_func=auth.required(MypageAccountName.as_view('mypage_account_name')))


# Mypage Account Name POST
app.add_url_rule(
    '/mypage/account/name/post',
    view_func=auth.required(MypageAccountNamePost.as_view('mypage_account_name_post')))


# Mypage Account Email
app.add_url_rule(
    '/mypage/account/email',
    view_func=auth.required(MypageAccountEmail.as_view('mypage_account_email')))


# Mypage Account Email POST
app.add_url_rule(
    '/mypage/account/email/post',
    view_func=auth.required(MypageAccountEmailPost.as_view('mypage_account_email_post')))


# Mypage Account Password
app.add_url_rule(
    '/mypage/account/password',
    view_func=auth.required(MypageAccountPassword.as_view('mypage_account_password')))


# Mypage Account Password POST
app.add_url_rule(
    '/mypage/account/password/post',
    view_func=auth.required(MypageAccountPasswordPost.as_view('mypage_account_password_post')))


# Topics Mypage List
app.add_url_rule(
    '/mypage/topics',
    view_func=auth.required(TopicsList.as_view('topics_list')))


# Topics Mypage Detail
app.add_url_rule(
    '/mypage/topics/<uuid>',
    view_func=auth.required(TopicsEdit.as_view('topics_edit')))


# Topics Edit
app.add_url_rule(
    '/mypage/topics/edit/<uuid>',
    view_func=auth.required(TopicsEditPost.as_view('topics_edit_post')))


# Topics Delete
app.add_url_rule(
    '/mypage/topics/delete/<uuid>',
    view_func=auth.required(TopicsDelete.as_view('topics_delete')))


# Topics Create
app.add_url_rule(
    '/mypage/topics/create',
    view_func=auth.required(TopicsCreate.as_view('topics_create')))


# Topics Create Post
app.add_url_rule(
    '/mypage/topics/create/post',
    view_func=auth.required(TopicsCreatePost.as_view('topics_create_post')))


# Comment Get
app.add_url_rule(
    '/comments/get/<uuid>',
    view_func=CommentGet.as_view('comment_get'))


# Comment List
app.add_url_rule(
    '/mypage/comments',
    view_func=auth.required(CommentList.as_view('comment_list')))


# Comment Edit
app.add_url_rule(
    '/mypage/comments/<uuid>',
    view_func=auth.required(CommentEdit.as_view('comment_edit')))


# Comment Edit POST
app.add_url_rule(
    '/mypage/comments/edit/<uuid>',
    view_func=auth.required(CommentEditPost.as_view('comment_edit_post')))


# Comment Delete
app.add_url_rule(
    '/mypage/comments/delete/<uuid>',
    view_func=auth.required(CommentDelete.as_view('comment_delete')))


# Comment Post
app.add_url_rule(
    '/comment/post/<uuid>',
    view_func=auth.required(CommentPost.as_view('comment_post')))


# Mypage Account Icon
app.add_url_rule(
    '/mypage/account/icon',
    view_func=auth.required(MypageAccountIcon.as_view('mypage_account_icon')))


# Mypage Account Icon POST
app.add_url_rule(
    '/mypage/account/icon/post',
    view_func=auth.required(MypageAccountIconPost.as_view('mypage_account_icon_post')))


# Mypage Account Delete
app.add_url_rule(
    '/mypage/account/delete',
    view_func=auth.required(MypageAccountDelete.as_view('mypage_account_delete')))


# Mypage Account Delete POST
app.add_url_rule(
    '/mypage/account/delete/post',
    view_func=auth.required(MypageAccountDeletePost.as_view('mypage_account_delete_post')))


# Login
app.add_url_rule(
    '/login',
    view_func=CredentialLogin.as_view('credential_login'))


# Logout
app.add_url_rule(
    '/logout',
    view_func=CredentialLogout.as_view('credential_logout'))


# Social Login Google Authorized
app.add_url_rule(
    '/social/google',
    view_func=CredentialGoogle.as_view('credential_google'))


# Social Login Google Authorized
app.add_url_rule(
    '/social/google/callback',
    view_func=CredentialGoogleAuthorized.as_view('credential_google_authorized'))


# Social Login Google Get Userinfo By Token
@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token'), ''


# Social Login Twitter Authorized
app.add_url_rule(
    '/social/twitter',
    view_func=CredentialTwitter.as_view('credential_twitter'))


# Social Login Twitter Authorized
app.add_url_rule(
    '/social/twitter/callback',
    view_func=CredentialTwitterAuthorized.as_view('credential_twitter_authorized'))


# Social Login Twitter Get Userinfo By Token
@twitter.tokengetter
def get_twitter_token():
    return session.get('oauth_token'), session.get('oauth_token_secret')


# Social Login Facebook Authorized
app.add_url_rule(
    '/social/facebook',
    view_func=CredentialFacebook.as_view('credential_facebook'))


# Social Login Facebook Authorized
app.add_url_rule(
    '/social/facebook/callback',
    view_func=CredentialFacebookAuthorized.as_view('credential_facebook_authorized'))


# Social Login Facebook Get Userinfo By Token
@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('facebook_oauth'), ''


# Social Login Github Authorized
app.add_url_rule(
    '/social/github',
    view_func=CredentialGithub.as_view('credential_github'))


# Social Login Github Authorized
app.add_url_rule(
    '/social/github/callback',
    view_func=CredentialGithubAuthorized.as_view('credential_github_authorized'))


# Social Login Github Get Userinfo By Token
@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token'), ''


# 404 Error Handler
@app.errorhandler(404)
def not_found(error):
    return Error.not_found()


# 500 Error Handler
@app.errorhandler(500)
def server_error(error):
    return Error.server_error(error)


# Server Error Handler
@app.errorhandler(Exception)
def server_error(error):
    return Error.server_error(error)


# Database Error Handler
@app.errorhandler(SQLAlchemyError)
def database_error(error):
    return Error.database_error(error)


# OAuth Error Handler
@app.errorhandler(OAuthException)
def server_error(error):
    return Error.server_error(error)


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:time.sleep(10)count += 1socketio.emit('my response',{'data': 'Server generated event', 'count': count},      namespace='/test')


@socketio.on('my event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response', {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my broadcast event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response', {'data': message['data'], 'count': session['receive_count']}, broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response', {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close room', namespace='/test')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my room event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})
