import webapp2
from webapp2_extras import auth

from app.lib.models.Users import User


class UserRequestHandler(webapp2.RequestHandler):
    pass

class ProfileHandler(UserRequestHandler):
    def get(self):
        print 123

    def drawProfilePage(self):
        print User.get_by_id(auth.get_auth().get_user_by_session()['user_id'])
        pass