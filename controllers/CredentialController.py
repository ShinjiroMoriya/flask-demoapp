from config import *
from models.user import User
from services.forms import *
from flask import render_template, request, redirect, url_for, escape, g
from flask.views import View


class CredentialLogin(View):

    # ログイン
    methods = ['GET', 'POST']

    def dispatch_request(self):

        if request.method == 'GET':

            return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

        # フォームバリデーション from services.forms
        form = LoginForm(request.form)

        # 入力Emailをセッションにセット
        session['email'] = form.email.data

        # フォームバリデーション return True
        if form.validate():

            try:

                # ユーザー情報取得
                user = User.query.filter_by(
                    email=escape(form.email.data),
                    valid=True
                ).first()

                if user:

                    if bcrypt.check_password_hash(user.password, form.password.data):

                        session.pop('email', None)
                        session['userid'] = user.userid
                        return redirect(url_for('mypage_index', _external=True, _scheme=app.config.get('SCHEME')))

                    else:

                        session['error'] = 'なんか違う'

                else:

                    session['error'] = '存在しません。誰ですか？'

            except Exception as e:

                app.logger.error(e)

                raise Exception('エラーが発生しました')

        if form.errors:

            session['error'] = error_message(form.errors)

        return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))


class CredentialGoogle(View):

    # グーグル認証ログイン
    def dispatch_request(self):

        return google.authorize(
            callback=url_for(
                'credential_google_authorized',
                _external=True,
                _scheme=app.config.get('SCHEME')
            )
        )


class CredentialGoogleAuthorized(View):

    # グーグル認証後、ユーザー情報取得処理
    def dispatch_request(self):

        try:

            res = google.authorized_response()

            if res is None:

                raise Exception('認証できませんでした。')

            # 取得したトークンをセッションに保存
            session['google_token'] = res['access_token']

            google_token = res['access_token']
            # トークンを利用してユーザー情報取得
            google_user = google.get('userinfo')
            # ユーザー情報取得用のトークンを削除
            session.pop('google_token', None)

            name = escape(google_user.data['name'])
            email = escape(google_user.data['email'])
            token = escape(google_token)

            # 既に登録しているユーザー判定
            already_user = User.query.filter_by(
                email=email,
                valid=True
            ).first()

            if already_user:

                # 既にGoogleログインしている場合はマイページへ
                if already_user.google_id:

                    session['userid'] = already_user.userid
                    return redirect(url_for('mypage_index', _external=True, _scheme=app.config.get('SCHEME')))

            # 既にローカルユーザーで登録している場合は、既存の名前を使用する
            # 取得したデータを登録時に引き継ぐ
            session['name'] = already_user.name if already_user else name
            session['email'] = email
            session['token'] = token
            session['type'] = 'google'

            return redirect(url_for('register_social', _external=True, _scheme=app.config.get('SCHEME')))

        except Exception as e:

            app.logger.error(e)

            raise Exception('エラーが発生しました')


class CredentialTwitter(View):

    # ツイッター認証ログイン
    def dispatch_request(self):

        return twitter.authorize(
            callback=url_for(
                'credential_twitter_authorized',
                next=request.args.get('next') or request.referrer or None,
                _external=True,
                _scheme=app.config.get('SCHEME')
            )
        )


class CredentialTwitterAuthorized(View):

    # ツイッター認証後、ユーザー情報取得処理
    def dispatch_request(self):

        try:

            res = twitter.authorized_response()

            if res is None:

                raise Exception('認証できませんでした。')

            # 取得したトークンでユーザー判別
            user = User.query.filter_by(
                twitter_id=res['oauth_token'],
                valid=True
            ).first()

            # 既に登録しているユーザーはマイページへ
            if user:

                session['userid'] = user.userid
                return redirect(url_for('mypage_index', _external=True, _scheme=app.config.get('SCHEME')))

            # セッションにTwitter Oauthをセットしトークンを取得する
            session['twitter_oauth'] = res['oauth_token']
            session['twitter_oauth_secret'] = res['oauth_token_secret']
            # ユーザー情報取得用のトークンを削除
            session.pop('twitter_oauth', None)
            session.pop('twitter_oauth_secret', None)

            # 取得したデータを登録時に引き継ぐ
            session['name'] = res['screen_name']
            session['token'] = res['oauth_token']
            session['type'] = 'twitter'

            return redirect(url_for('register_social', _external=True, _scheme=app.config.get('SCHEME')))

        except Exception as e:

            app.logger.error(e)

            raise Exception('エラーが発生しました')


class CredentialFacebook(View):

    # フェイスブック認証ログイン
    def dispatch_request(self):

        return facebook.authorize(
            callback=url_for(
                'credential_facebook_authorized',
                next=request.args.get('next') or request.referrer or None,
                _external=True,
                _scheme=app.config.get('SCHEME')
            )
        )


class CredentialFacebookAuthorized(View):

    # フェイスブック認証後、ユーザー情報取得処理
    def dispatch_request(self):

        try:

            res = facebook.authorized_response()

            if res is None:

                raise Exception('認証できませんでした。')

            session['facebook_oauth'] = res['access_token']

            facebook_user = facebook.get('/me')

            name = facebook_user.data['name']
            email = facebook_user.data['email']

            already_user = User.query.filter_by(
                email=email,
                valid=True
            ).first()

            user = User.query.filter_by(
                facebook_id=res['access_token'],
                valid=True
            ).first()

            if user:

                session['userid'] = user.userid
                return redirect(url_for('mypage_index', _external=True, _scheme=app.config.get('SCHEME')))

            # 既にローカルユーザーで登録している場合は、既存の名前を使用する
            # 取得したデータを登録時に引き継ぐ
            session['name'] = already_user.name if already_user else name
            session['email'] = email
            session['token'] = res['access_token']
            session['type'] = 'facebook'

            return redirect(url_for('register_social', _external=True, _scheme=app.config.get('SCHEME')))

        except Exception as e:

            app.logger.error(e)

            raise Exception('エラーが発生しました')


class CredentialGithub(View):

    # Github認証ログイン
    def dispatch_request(self):

        return github.authorize(
            callback=url_for(
                'credential_github_authorized',
                _external=True,
                _scheme=app.config.get('SCHEME')
            )
        )


class CredentialGithubAuthorized(View):

    # Github認証後、ユーザー情報取得処理
    def dispatch_request(self):

        try:

            res = github.authorized_response()

            if res is None:

                raise Exception('認証できませんでした。')

            session.set('github_token', res['access_token'], ex=1)

            github_user = github.get('user')

            name = github_user.data['name']
            email = github_user.data['email']

            already_user = User.query.filter_by(
                email=email,
                valid=True
            ).first()

            user = User.query.filter_by(
                github_id=res['access_token'],
                valid=True
            ).first()

            if user:

                session['userid'] = user.userid
                return redirect(url_for('mypage_index', _external=True, _scheme=app.config.get('SCHEME')))

            session.hmset('social_data', {
                'name': already_user.name if already_user else name,
                'email': email,
                'token': res['access_token'],
                'type': 'github',
            })

            return redirect(url_for('register_social', _external=True, _scheme=app.config.get('SCHEME')))

        except Exception as e:

            app.logger.error(e)

            raise Exception('エラーが発生しました')


class CredentialLogout(View):

    # ログアウト
    def dispatch_request(self):

        session.clear()
        return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))
