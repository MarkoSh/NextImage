import os

from google.appengine.api import users
import webapp2
import jinja2
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError

from models.Users import User


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
TEMPLATES_PATH = "tmpls/"

app_config = {
        'webapp2_extras.auth': {
        'user_model': User
        },
        'webapp2_extras.sessions': {
            'secret_key': 'mimimimimimimimi'
        }
    }

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
                'title': 'Login page',
                'login': False
            }
        user = users.get_current_user()
        print user
        if user:
            template_values = {
                'title': 'Hello there, ' + user.nickname(),
                'login': True
            }
        template = JINJA_ENVIRONMENT.get_template(TEMPLATES_PATH + '_layout.html')
        self.response.write(template.render(template_values))

    def post(self):
        if self.request.get('login'):
            template_values = {
                'title': 'Login page',
                'login': False
            }
            login = self.request.get('login')
            password = self.request.get('password')
            if "checkname" in self.request.path:
                print 'Checking name {}...'.format(login)

            if self.request.get('sigbtn'):
                print 'Registering user {}...'.format(login)
                if "@" in login and password.__len__() > 6:
                    unique_properties = ['email_address']
                    user = User.create_user(login, unique_properties, email_address=login, password_raw=password,
                                            verified=False)
                    if not user[0]:
                        template_values = {
                            'title': 'May be you can try log in instead?',
                            'login': False
                        }
                        print 'Unable to create user {}, duplicating key {}'.format(login, user[1])
                    else:
                        template_values = {
                            'title': 'Now you can create everything',
                            'login': True
                        }
                        print '6sfull creating user {}'.format(login)


            if self.request.get('logbtn'):
                print 'Logging as {}...'.format(login)
                try:
                    print '6sfull logging user {} '.format(login)
                    self.redirect('/')
                except (InvalidPasswordError, InvalidAuthIdError) as e:
                    template_values = {
                            'title': 'Ouch, you may be wrong',
                            'login': False
                        }
                    print "Auth error {}".format(type(e))
            template = JINJA_ENVIRONMENT.get_template(TEMPLATES_PATH + '_layout.html')
            self.response.write(template.render(template_values))



app = webapp2.WSGIApplication([
                                  ('/', MainHandler),
                                  ('/login', MainHandler),
                                  ('/checkname', MainHandler),
], debug=True, config = app_config)
