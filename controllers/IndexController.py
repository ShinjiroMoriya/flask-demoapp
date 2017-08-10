from config import *
from models.user import User
from services.forms import *
from flask import render_template, escape, redirect, url_for, request
from flask.views import View


class Index(View):

    def dispatch_request(self):

        if session.get('userid'):

            return redirect(url_for('mypage_index', _external=True, _scheme=app.config.get('SCHEME')))

        data = {
            'title': 'Hello World',
            'email': session.get('email'),
            'error': session.get('error')
        }
        session.clear()

        return render_template('index/index.html', data=data)


class IndexValid(View):

    # Email認証用の処理
    def dispatch_request(self):

        # パラメーター token 取得
        token = escape(request.args.get('token'))

        if token is None:

            return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

        try:

            user = User.query.filter_by(
                token=token,
                valid=False
            ).first()

            if user:

                user.valid = True
                db.session.commit()

            else:

                return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

        except Exception as e:

            db.session.rollback()

            app.logger.error(e)

            raise Exception('エラーが発生しました')

        session['userid'] = user.userid

        return redirect(url_for('mypage_index', _external=True, _scheme=app.config.get('SCHEME')))


class IndexMailValid(View):

    # Email変更時の認証用の処理
    def dispatch_request(self):

        # パラメーター token 取得
        token = escape(request.args.get('token'))

        if token is None:

            return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

        try:

            user = User.query.filter_by(
                token=token,
                valid=True
            ).first()

            user.email = user.temporary
            user.temporary = None

            db.session.commit()

        except Exception as e:

            db.session.rollback()

            app.logger.error(e)

            raise Exception('エラーが発生しました')

        session['userid'] = user.userid

        return redirect(url_for('mypage_index', _external=True, _scheme=app.config.get('SCHEME')))


class IndexPassword(View):

    # パスワード再登録
    def dispatch_request(self):

        data = {
            'title': 'Password | Hello World',
            'error': session.get('error')
        }

        session.pop('error', None)

        return render_template('index/password.html', data=data)


class IndexPasswordRemind(View):

    # パスワード再登録 メール送信
    methods = ['GET', 'POST']

    def dispatch_request(self):

        if request.method == 'GET':

            return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

        form = EmailForm(request.form)

        if form.validate():

            try:
                # ユーザー登録されているか判定
                user = User.query.filter_by(
                    email=escape(form.email.data),
                    valid=True
                ).first()

                # ユーザーが存在している場合は戻す
                if user:
                    # メール送信データ
                    maildata = {
                        'name': user.name,
                        'token': user.token,
                        'url': app.config.get('URL')
                    }
                    message = sendgrid.Mail(
                        to=form.email.data,
                        subject='Password',
                        html=render_template(
                            'emails/password.html', data=maildata),
                        from_name='Hello World',
                        from_email=app.config.get('FROM_EMAIL')
                    )
                    status, msg = sg.send(message)

                    app.logger.error(msg)

                    db.session.commit()

                    return redirect(url_for('send', _external=True, _scheme=app.config.get('SCHEME')))

                else:

                    session['error'] = '登録されていないです。'

                    return redirect(url_for('index_password'))

            except Exception as e:

                db.session.rollback()

                app.logger.error(e)

                raise Exception('エラーが発生しました')

        if form.errors:

            session['error'] = error_message(form.errors)

        return redirect(url_for('index_password'))


class IndexPasswordChange(View):

    # パスワード再登録 入力画面
    def dispatch_request(self):
        # パラメーター token 取得
        token = escape(request.args.get('token'))

        if token is None:

            return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

        try:

            user = User.query.filter_by(
                token=token,
                valid=True
            ).first()

            if user is None:

                raise Exception('無効な処理です。')

        except Exception as e:

            db.session.rollback()

            app.logger.error(e)

            raise Exception('エラーが発生しました')

        data = {
            'title': 'Passwrd Change | Hello World',
            'error': session.get('error'),
            'token': escape(request.args.get('token'))
        }

        session.pop('error', None)

        return render_template('index/password_change.html', data=data)


class IndexPasswordChangePost(View):

    # パスワード再登録 送信
    methods = ['GET', 'POST']

    def dispatch_request(self):

        if request.method == 'GET':

            return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

        form = PasswordRemindForm(request.form)

        if form.validate():

            try:
                # ユーザー登録されているか判定
                user = User.query.filter_by(
                    token=escape(form.token.data),
                    valid=True
                ).first()

                # ユーザーが存在している場合は戻す
                if user:

                    user.password = bcrypt.generate_password_hash(
                        form.password.data)

                    session['userid'] = user.userid

                    db.session.commit()

                    return redirect(url_for('mypage_index', _external=True, _scheme=app.config.get('SCHEME')))

                else:

                    session['error'] = '登録されていないです。'

                    return redirect(url_for('index_password', _external=True, _scheme=app.config.get('SCHEME')))

            except Exception as e:

                db.session.rollback()

                app.logger.error(e)

                raise Exception('エラーが発生しました')

        if form.errors:

            session['error'] = error_message(form.errors)


class IndexSend(View):

    # メール送信後ページ
    def dispatch_request(self):

        data = {
            'title': 'Send | Hello World',
        }
        return render_template('index/send.html', data=data)
