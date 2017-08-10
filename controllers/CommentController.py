from config import *
from models.topic import Topic
from models.comment import Comment
from services.forms import *
from services.pager import Pagination
from flask import render_template, request, redirect, url_for, escape, g, Markup, jsonify
from flask.views import View
import re
import markdown


class CommentList(View):

    def dispatch_request(self):

        page = request.args.get('page') if request.args.get('page') else 1

        if re.match(r"\d", str(page)) is None:
            return redirect('/mypage/comments')

        per = int(app.config.get('POST_PER_PAGE')) * (int(page) - 1)
        count = count = Comment.query.filter_by(
            userid=g.user['userid'], comment_delete=False).count()
        comments = Comment.query.filter_by(userid=g.user['userid'], comment_delete=False)\
            .order_by(Comment.commentid.desc()).offset(per).limit(int(app.config.get('POST_PER_PAGE')))

        per_page = per if per else int(app.config.get('POST_PER_PAGE'))

        pagination = Pagination(page=int(page), per_page=per_page, total_count=int(
            count), slug='/mypage/comments')

        data = {
            'title': 'Comment | Mypage | Hello World',
            'comments': comments,
            'next': pagination.next(),
            'prev': pagination.prev(),
        }

        return render_template('comments/list.html', data=data)


class CommentPost(View):

    methods = ['GET', 'POST']

    def dispatch_request(self, uuid):

        if request.method == 'GET':

            return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

        form = CommentForm(request.form)

        if form.validate():

            try:

                topic = Topic.query.filter_by(
                    topicuuid=uuid, topic_delete=False).first()

                if topic is None:

                    return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

                comment = Comment(
                    comment=form.comment.data,
                    userid=session.get('userid'),
                    topicid=topic.topicid,
                    comment_markdown=Markup(
                        markdown.markdown(form.comment.data))
                )

                db.session.add(comment)
                db.session.commit()

                session['comment_add'] = True

                return redirect('/topics/' + uuid)

            except Exception as e:

                db.session.rollback()

                app.logger.error(e)

                raise Exception('エラーが発生しました')

        if form.errors:

            session['error'] = error_message(form.errors)

            return redirect('/topics/' + escape(uuid))


class CommentEdit(View):

    def dispatch_request(self, uuid):

        comment = Comment.query.filter_by(
            commentuuid=uuid, comment_delete=False).first()

        if comment is None:

            return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

        data = {
            'title': 'Comment | Hello World',
            'comment': comment,
            'error': session.get('error')
        }

        session.pop('error', None)

        return render_template('comments/edit.html', data=data)


class CommentEditPost(View):

    methods = ['GET', 'POST']

    def dispatch_request(self, uuid):

        if request.method == 'GET':

            return redirect(url_for('index', _external=True, _scheme=app.config.get('SCHEME')))

        form = CommentForm(request.form)

        if form.validate():

            try:

                comment = Comment.query.filter_by(commentuuid=uuid).first()

                if comment is None:

                    redirect(url_for('index', _external=True,
                                     _scheme=app.config.get('SCHEME')))

                comment.comment = form.comment.data
                comment.comment_markdown = Markup(
                    markdown.markdown(form.comment.data))

                db.session.commit()

                return redirect(url_for('comment_list', _external=True, _scheme=app.config.get('SCHEME')))

            except Exception as e:

                db.session.rollback()

                app.logger.error(e)

                raise Exception('エラーが発生しました')

        if form.errors:

            session['error'] = error_message(form.errors)

            return redirect('/mypage/comments/' + uuid)


class CommentDelete(View):

    def dispatch_request(self, uuid):

        comment = Comment.query.filter_by(
            commentuuid=uuid, comment_delete=False).first()

        if comment is None:

            return redirect(url_for('comment_list', _external=True, _scheme=app.config.get('SCHEME')))

        try:

            comment.comment_delete = True

            db.session.commit()

        except Exception as e:

            db.session.rollback()

            app.logger.error(e)

            raise Exception('エラーが発生しました')

        return redirect(url_for('comment_list', _external=True, _scheme=app.config.get('SCHEME')))


class CommentGet(View):

    def dispatch_request(self, uuid):

        topic = Topic.query.filter_by(
            topicuuid=uuid, topic_delete=False).first()

        if topic is None:
            return None

        comment = Comment.query.filter_by(topicid=topic.topicid, comment_delete=False).order_by(
            Comment.commentid.desc()).first()

        if comment is None:
            return None

        data = {
            'icon': comment.user.icon,
            'user': comment.user.name,
            'comment': comment.comment_markdown,
            "date": comment.created
        }

        return jsonify(data)
