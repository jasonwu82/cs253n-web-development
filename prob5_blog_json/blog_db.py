

from google.appengine.ext import ndb


class Post(ndb.Model):
    subject = ndb.StringProperty()
    content = ndb.StringProperty()