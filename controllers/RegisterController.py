from config import *
from services.forms import *
from models.user import User
from flask import render_template, request, redirect, url_for, escape
from flask.views import View


class RegisterIndex(View):

    def dispatch_request(self):

        data = {
            'title': 'Register | Hello World',
            'error': session.get('error')
        }

        session.pop('error', None)

        return render_template('register/index.html', data=data)


class RegisterCreate(View):

    methods = ['GET', 'POST']

    def dispatch_request(self):

        if request.method == 'GET':

            return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

        form = RegisterForm(request.form)

        if form.validate():

            try:

                # ユーザー登録されているか判定
                user = User.query.filter_by(
                    email=escape(form.email.data),
                    valid=True
                ).first()

                # ユーザーが存在している場合は戻す
                if user:

                    session['error'] = '既に登録されています。'
                    return redirect(url_for('register', _external=True, _scheme=app.config.get('SCHEME')))

                user = User(
                    name=form.name.data,
                    email=form.email.data,
                    password=form.password.data,
                )
                db.session.add(user)

                # メール送信データ
                maildata = {
                    'name': user.name,
                    'token': user.token,
                    'url': app.config.get('URL')
                }
                message = sendgrid.Mail(
                    to=form.email.data,
                    subject='Please Authenticate',
                    html=render_template(
                        'emails/register.html', data=maildata),
                    from_name='Hello World',
                    from_email=app.config.get('FROM_EMAIL')
                )
                status, msg = sg.send(message)

                app.logger.error(msg)

                db.session.commit()

                return redirect(url_for('send', _external=True, _scheme=app.config.get('SCHEME')))

            except Exception as e:

                db.session.rollback()

                app.logger.error(e)

                raise Exception('エラーが発生しました')

        if form.errors:

            session['error'] = error_message(form.errors)

        return redirect(url_for('register', _external=True, _scheme=app.config.get('SCHEME')))


class RegisterSocial(View):

    def dispatch_request(self):

        # ソーシャルデータ セッションから取得
        if session.get('type'):

            data = {
                'title': 'Register | Hello World',
                'name': session.get('name'),
                'email': session.get('email'),
                'type': session.get('type'),
                'error': session.get('error')
            }

            session.pop('error', None)

            return render_template('register/social.html', data=data)

        return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))


class RegisterSocialCreate(View):

    methods = ['GET', 'POST']

    def dispatch_request(self):

        if request.method == 'GET':

            return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

        form = RegisterSocialForm(request.form)

        if form.validate():

            try:

                # ソーシャルデータ セッションがない場合
                if session.get('type') is None:

                    session['error'] = '無効な処理です。'
                    return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

                # 既に登録しているユーザー取得する
                already_user = User.query.filter_by(
                    email=escape(form.email.data),
                    valid=True
                ).first()

                # 既に登録しているユーザーの場合は無効
                if already_user:

                    # ソーシャルデータ削除
                    session.pop('name', None)
                    session.pop('email', None)
                    session.pop('token', None)
                    session.pop('type', None)

                    session['error'] = '既に登録されています。'
                    return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

                else:

                    # 新規の場合はメール認証を行う
                    user = User(
                        name=form.name.data,
                        email=form.email.data,
                        google_id=session.get('token') if session.get(
                            'type') == 'google' else None,
                        twitter_id=session.get('token') if session.get(
                            'type') == 'twitter' else None,
                        facebook_id=session.get('token') if session.get(
                            'type') == 'facebook' else None,
                        github_id=session.get('token') if session.get(
                            'type') == 'github' else None,
                    )
                    db.session.add(user)

                    # メール送信データ
                    maildata = {
                        'name': user.name,
                        'token': user.token,
                        'url': app.config.get('URL')
                    }
                    message = sendgrid.Mail(
                        to=form.email.data,
                        subject='Please Authenticate',
                        html=render_template(
                            'emails/register.html', data=maildata),
                        from_name='Hello World',
                        from_email=app.config.get('FROM_EMAIL')
                    )

                    status, msg = sg.send(message)
                    app.logger.error(msg)

                    # ソーシャルデータ削除
                    session.pop('name', None)
                    session.pop('email', None)
                    session.pop('token', None)
                    session.pop('type', None)

                    # 新規ユーザー作成
                    db.session.commit()

                    return redirect(url_for('send', _external=True, _scheme=app.config.get('SCHEME')))

            except Exception as e:

                db.session.rollback()

                app.logger.error(e)

                raise Exception('エラーが発生しました')

        if form.errors:

            session['error'] = error_message(form.errors)

        return redirect(url_for('register_social', _external=True, _scheme=app.config.get('SCHEME')))
