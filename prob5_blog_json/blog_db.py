

from google.appengine.ext import ndb


class Post(ndb.Model):
    subject = ndb.StringProperty()
    content = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)