from app import app
from datetime import datetime, timedelta, tzinfo

# 日本時間


class jptime(tzinfo):

    def utcoffset(self, dt):
        return timedelta(hours=9)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return 'jptime'
