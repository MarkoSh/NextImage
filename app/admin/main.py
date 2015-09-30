import webapp2
import jinja2
from webapp2_extras import sessions
from webapp2_extras.users import users

from app.lib.models.Users import Admin, User
from app.frypic.UserHandler import UserRequestHandler


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

app_config = {
        'webapp2_extras.auth': {
            'user_model': Admin
        },
        'webapp2_extras.sessions': {
            'secret_key': 'mimimimimimimimi'
        }
    }

class MainHandler(UserRequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    def get(self):
        user = users.get_current_user()
        if not user:
            self.response.write('<a href="{}">login</a>'.format(users.create_login_url('/admin')))
        else:
            if not users.is_current_user_admin():
                self.response.write('<a href="{}">You are not admin. logout</a>'.format(users.create_logout_url('/admin')))
            else:
                print User.query().fetch()
                self.response.write('<a href="{}">You are admin. logout</a>'.format(users.create_logout_url('/admin')))

app = webapp2.WSGIApplication([
                                  ('/admin', MainHandler)
], debug=True, config = app_config)