import os

from google.appengine.api import users
import webapp2
import jinja2

from models.Users import User


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
TEMPLATES_PATH = "tmpls/"

app_config = {
        'webapp2_extras.auth': {
        'user_model': User
    }
}

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
                'title': 'Login page',
                'login': False
            }
        user = users.get_current_user()
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
                users = User.query(User.name == login).fetch()
                if len(users):
                    template_values = {
                        'title': 'Sorry, but you already here...',
                        'login': False
                    }

            if self.request.get('logbtn'):
                print 'Logging as {}...'.format(login)
                user = User.query(User.name == login, User.password == password).fetch(1)
                if len(user):
                    template_values = {
                        'title': 'Hi there',
                        'login': True
                    }
                else:
                    user = User.query(User.name == login).fetch()
                    if len(user):
                        print 'Incorret password for {}'.format(login)
                        template_values = {
                            'title': 'Ouch, you may be wrong',
                            'login': False
                        }
                    else:
                        print 'User {} not found'.format(login)
                        template_values = {
                            'title': 'Hey, you not here yet, wanna sign in?',
                            'login': False
                        }
            template = JINJA_ENVIRONMENT.get_template(TEMPLATES_PATH + '_layout.html')
            self.response.write(template.render(template_values))



app = webapp2.WSGIApplication([
                                  ('/', MainHandler),
                                  ('/login', MainHandler),
                                  ('/checkname', MainHandler),
], debug=True, config = app_config)
