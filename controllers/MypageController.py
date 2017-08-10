from config import *
from models.user import User
from services.forms import *
from flask import render_template, request, redirect, url_for, escape, g
from flask.views import View


class MypageIndex(View):

    def dispatch_request(self):

        data = {
            'title': 'Mypage | Hello World',
            'name': g.user['name'],
            'icon': g.user['icon']
        }

        session.pop('error', None)

        return render_template('mypage/index.html', data=data)


class MypageAccount(View):

    def dispatch_request(self):

        data = {
            'title': 'Account | Hello World'
        }

        return render_template('mypage/account.html', data=data)


class MypageAccountName(View):

    def dispatch_request(self):

        data = {
            'title': 'Name | Account | Hello World',
            'name': g.user['name'],
            'error': session.get('error')
        }

        session.pop('error', None)

        return render_template('mypage/account_name.html', data=data)


class MypageAccountNamePost(View):

    methods = ['GET', 'POST']

    def dispatch_request(self):

        if request.method == 'GET':

            return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

        form = UpdateNameForm(request.form)

        if form.validate():

            try:

                user = User.query.get(g.user['userid'])

                user.name = form.name.data
                user.modified = datetime.now(
                    tz=jptime()).strftime('%Y-%m-%d %H:%M:%S')

                db.session.commit()

            except Exception as e:

                db.session.rollback()

                app.logger.error(e)

                raise Exception('エラーが発生しました')

            return redirect(url_for('mypage_index', _external=True, _scheme=app.config.get('SCHEME')))

        if form.errors:

            session['error'] = error_message(form.errors)

            return redirect(url_for('mypage_account_name', _external=True, _scheme=app.config.get('SCHEME')))


class MypageAccountEmail(View):

    def dispatch_request(self):

        data = {
            'title': 'Name | Account | Hello World',
            'email': g.user['email'],
            'error': session.get('error')
        }

        session.pop('error', None)

        return render_template('mypage/account_email.html', data=data)


class MypageAccountEmailPost(View):

    methods = ['GET', 'POST']

    def dispatch_request(self):

        if request.method == 'GET':

            return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

        form = EmailForm(request.form)

        if form.validate():

            try:

                user = User.query.get(g.user['userid'])

                if user.email == form.email.data:

                    session['error'] = 'Emailが同じです。'
                    return redirect(url_for('mypage_account_email', _external=True, _scheme=app.config.get('SCHEME')))

                already_user = User.query.filter_by(
                    email=escape(form.email.data),
                ).first()

                if already_user:

                    session['error'] = '既に使用されています。'
                    return redirect(url_for('mypage_account_email', _external=True, _scheme=app.config.get('SCHEME')))

                user.temporary = form.email.data
                user.modified = datetime.now(
                    tz=jptime()).strftime('%Y-%m-%d %H:%M:%S')

                maildata = {
                    'name': user.name,
                    'token': user.token,
                    'url': app.config.get('URL')
                }
                message = sendgrid.Mail(
                    to=form.email.data,
                    subject='Please Email Authenticate',
                    html=render_template(
                        'emails/email_change.html', data=maildata),
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

            return redirect(url_for('mypage_account_email', _external=True, _scheme=app.config.get('SCHEME')))


class MypageAccountPassword(View):

    def dispatch_request(self):

        data = {
            'title': 'Password | Account | Hello World',
            'error': session.get('error')
        }

        session.pop('error', None)

        return render_template('mypage/account_password.html', data=data)


class MypageAccountPasswordPost(View):

    methods = ['GET', 'POST']

    def dispatch_request(self):

        if request.method == 'GET':

            return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

        form = PasswordForm(request.form)

        if form.validate():

            try:

                user = User.query.get(g.user['userid'])

                user.password = bcrypt.generate_password_hash(
                    form.password.data)
                user.modified = datetime.now(
                    tz=jptime()).strftime('%Y-%m-%d %H:%M:%S')

                db.session.commit()

                return redirect(url_for('mypage_account', _external=True, _scheme=app.config.get('SCHEME')))

            except Exception as e:

                db.session.rollback()

                app.logger.error(e)

                raise Exception('エラーが発生しました')

        if form.errors:

            session['error'] = error_message(form.errors)

            return redirect(url_for('mypage_account_password', _external=True, _scheme=app.config.get('SCHEME')))


class MypageAccountIcon(View):

    def dispatch_request(self):

        data = {
            'title': 'Icon | Account | Hello World',
            'name': g.user['name'],
            'icon': g.user['icon'],
            'error': session.get('error')
        }

        session.pop('error', None)

        return render_template('mypage/account_icon.html', data=data)


class MypageAccountIconPost(View):

    methods = ['GET', 'POST']

    def dispatch_request(self):

        if request.method == 'GET':

            return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

        file = request.files['icon']

        file_name, ext = os.path.splitext(file.filename)

        if file_ext_check(ext, 'image'):

            session['error'] = '[.jpg, .jpeg, .png, .gif]のみ対応です。'

            return redirect(url_for('mypage_account_icon', _external=True, _scheme=app.config.get('SCHEME')))

        if 5000000 < len(file.read()):

            session['error'] = 'データの容量は5MBまでです。'

            return redirect(url_for('mypage_account_icon', _external=True, _scheme=app.config.get('SCHEME')))

        if file:

            try:

                upload_result = upload(file)
                images, options = cloudinary_url(upload_result[
                                                 'public_id'], format="jpg", crop="fill", width=800, height=800, secure=True)

                user = User.query.get(g.user['userid'])

                # 前の画像は削除
                if user.icon_id:
                    delete_resources([user.icon_id])

                user.icon = images
                user.icon_id = upload_result['public_id']
                user.modified = datetime.now(
                    tz=jptime()).strftime('%Y-%m-%d %H:%M:%S')

                db.session.commit()

            except Exception as e:

                db.session.rollback()

                app.logger.error(e)

                raise Exception('エラーが発生しました')

        else:

            session['error'] = 'ファイルが選択されていません。'

        return redirect(url_for('mypage_account_icon', _external=True, _scheme=app.config.get('SCHEME')))


class MypageAccountDelete(View):

    def dispatch_request(self):

        data = {
            'title': 'Delete | Account | Hello World',
            'error': session.get('error')
        }

        session.pop('error', None)

        return render_template('mypage/account_delete.html', data=data)


class MypageAccountDeletePost(View):

    methods = ['GET', 'POST']

    def dispatch_request(self):

        if request.method == 'GET':

            return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

        form = PasswordForm(request.form)

        # フォームバリデーション return True
        if form.validate():

            if bcrypt.check_password_hash(user.password, form.password.data):

                try:

                    user = User.query.get(g.user['userid'])

                    user.valid = False
                    user.password = None

                    session.clear()

                    db.session.commit()
                    return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

                except Exception as e:

                    db.session.rollback()

                    app.logger.error(e)

                    raise Exception('エラーが発生しました')

            else:

                session['error'] = 'なんか違う'
                return redirect(url_for('mypage_account_delete', _external=True, _scheme=app.config.get('SCHEME')))

        if form.errors:

            session['error'] = error_message(form.errors)

            return redirect(url_for('mypage_account_delete', _external=True, _scheme=app.config.get('SCHEME')))
