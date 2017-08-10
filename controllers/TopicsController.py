from config import *
from models.user import User
from models.topic import Topic
from models.comment import Comment
from services.forms import *
from services.pager import Pagination
from flask import render_template, request, redirect, url_for, escape, g, Markup
from flask.views import View
import re
import markdown


class TopicsList(View):

    def dispatch_request(self):

        # パラメーター page 取得

        page = request.args.get('page') if request.args.get('page') else 1

        if re.match(r"\d", str(page)) is None:
            return redirect('/mypage/topics')

        per = int(app.config.get('POST_PER_PAGE')) * (int(page) - 1)
        count = count = Topic.query.filter_by(
            userid=g.user['userid'], topic_delete=False).count()
        topics = Topic.query.filter_by(userid=g.user['userid'], topic_delete=False)\
            .order_by(Topic.topicid.desc()).offset(per).limit(int(app.config.get('POST_PER_PAGE')))

        per_page = per if per else int(app.config.get('POST_PER_PAGE'))

        pagination = Pagination(page=int(page), per_page=per_page, total_count=int(
            count), slug='/mypage/topics')

        data = {
            'title': 'Topics | Mypage | Hello World',
            'topics': topics,
            'next': pagination.next(),
            'prev': pagination.prev(),
        }

        return render_template('topics/list.html', data=data)


class TopicsCreate(View):

    def dispatch_request(self):

        data = {
            'title': 'Create | Topics | Mypage | Hello World',
            'error': session.get('error')
        }

        session.pop('error', None)

        return render_template('topics/create.html', data=data)


class TopicsCreatePost(View):

    methods = ['GET', 'POST']

    def dispatch_request(self):

        if request.method == 'GET':

            return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

        form = TopicForm(request.form)

        if form.validate():

            try:

                topics = Topic(
                    userid=g.user['userid'],
                    topic=form.topic.data,
                    topic_markdown=Markup(markdown.markdown(form.topic.data))
                )

                db.session.add(topics)
                db.session.commit()

                return redirect(url_for('topics_list', _external=True, _scheme=app.config.get('SCHEME')))

            except Exception as e:

                db.session.rollback()

                app.logger.error(e)

                raise Exception('エラーが発生しました')

        if form.errors:

            session['error'] = error_message(form.errors)

            return redirect(url_for('topics_create', _external=True, _scheme=app.config.get('SCHEME')))


class TopicsEdit(View):

    def dispatch_request(self, uuid):

        topic = Topic.query.filter_by(
            topicuuid=uuid, topic_delete=False).first()

        if topic is None:

            return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

        data = {
            'title': 'Topics | Hello World',
            'topic': topic,
            'back': escape(request.args.get('detail')),
            'error': session.get('error')
        }

        session.pop('error', None)

        return render_template('topics/edit.html', data=data)


class TopicsEditPost(View):

    methods = ['GET', 'POST']

    def dispatch_request(self, uuid):

        if request.method == 'GET':

            return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

        form = TopicForm(request.form)

        if form.validate():

            try:

                topic = Topic.query.filter_by(topicuuid=uuid).first()

                if topic is None:

                    redirect(url_for('index', _external=True,
                                     _scheme=app.config.get('SCHEME')))

                topic.topic = form.topic.data
                topic.topic_markdown = Markup(
                    markdown.markdown(form.topic.data))

                db.session.commit()

                if escape(request.args.get('detail')) == 'back':

                    return redirect('/topics/' + uuid)

                return redirect(url_for('topics_list', _external=True, _scheme=app.config.get('SCHEME')))

            except Exception as e:

                db.session.rollback()

                app.logger.error(e)

                raise Exception('エラーが発生しました')

        if form.errors:

            session['error'] = error_message(form.errors)

            return redirect('/mypage/topics/' + uuid)


class TopicsDelete(View):

    def dispatch_request(self, uuid):

        topic = Topic.query.filter_by(
            topicuuid=uuid, topic_delete=False).first()

        if topic is None:

            return redirect(url_for('topics_edit_list', _external=True, _scheme=app.config.get('SCHEME')))

        try:

            topic.topic_delete = True

            db.session.commit()

        except Exception as e:

            db.session.rollback()

            app.logger.error(e)

            raise Exception('エラーが発生しました')

        return redirect(url_for('topics_list', _external=True, _scheme=app.config.get('SCHEME')))


class TopicsIndex(View):

    def dispatch_request(self):

        # パラメーター page 取得

        page = request.args.get('page') if request.args.get('page') else 1

        if re.match(r"\d", str(page)) is None:
            return redirect('/topics')

        per = int(app.config.get('POST_PER_PAGE')) * (int(page) - 1)
        count = Topic.query.filter_by(topic_delete=False).count()

        topics = Topic.query.filter_by(topic_delete=False).order_by(
            Topic.topicid.desc()).offset(per).limit(int(app.config.get('POST_PER_PAGE')))

        per_page = per if per else int(app.config.get('POST_PER_PAGE'))

        pagination = Pagination(
            page=int(page), per_page=per_page, total_count=int(count), slug='/topics')

        data = {
            'title': 'Topics | Hello World',
            'topics': topics,
            'next': pagination.next(),
            'prev': pagination.prev()
        }

        return render_template('topics/index.html', data=data)


class TopicsDetail(View):

    def dispatch_request(self, uuid):

        topic = Topic.query.filter_by(
            topicuuid=uuid, topic_delete=False).first()
        comments = Comment.query.filter_by(
            topicid=topic.topicid, comment_delete=False).order_by(Comment.commentid.asc())

        if topic is None:

            return redirect('/topics')

        data = {
            'title': 'Topics | Hello World',
            'topic': topic,
            'logged': session.get('userid'),
            'comments': comments,
            'error': session.get('error'),
            'nowtime': datetime.now(tz=jptime()).strftime('%Y-%m-%d %H:%M:%S'),
            'comment_add': session.get('comment_add')
        }

        session.pop('comment_add', None)
        session.pop('error', None)

        return render_template('topics/detail.html', data=data)
