from google.appengine.ext import ndb
import hashlib


ENCRYPT_SEED = "haha"

def user_encrypt_token(username):
    str = username + ENCRYPT_SEED
    return hashlib.sha256(str).hexdigest()

def verify_token(username,token):
    str = username + ENCRYPT_SEED
    if hashlib.sha256(str).hexdigest() == token:
        return True
    return False


class User(ndb.Model):
    username = ndb.StringProperty(indexed=True)
    password = ndb.StringProperty()