from app import app
from jinja2 import evalcontextfilter, Markup, escape
import datetime
import os
import re


@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    _paragraph_re = re.compile(r'(?:\r\n|\r(?!\n)|\n){2,}')
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace(u'\r\n', u'<br>')
                          for p in _paragraph_re.split(value))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


def _filter_space_delete(value, num=None):

    value = re.sub(r'[\s\r\n]+', '', value)

    length = len(value)

    if num and num < length:
        value = value[:num] + '…'

    return value

app.jinja_env.filters['delete_space'] = _filter_space_delete


def _filter_datetime(date, fmt='%Y-%m-%d %H:%M'):

    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return date.strftime(fmt)

app.jinja_env.filters['datetime'] = _filter_datetime


def _getenv(value, key):

    return os.environ.get(key, value)

app.jinja_env.filters['getenv'] = _getenv


def _linktarget(value):

    return re.sub(r'<a', '<a target="_blank"', value)

app.jinja_env.filters['linktarget'] = _linktarget


def _thumbnail(img):

    return img.replace(u'h_800,w_800', u'h_100,w_100')

app.jinja_env.filters['thumbnail'] = _thumbnail
