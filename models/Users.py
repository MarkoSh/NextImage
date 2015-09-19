import webapp2_extras.appengine.auth.models as auth_models
from google.appengine.ext import ndb

class User(auth_models.User):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    phone = ndb.IntegerProperty()