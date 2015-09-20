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
        if "checkname" in self.request.path:
            login = self.request.POST['login'].strip()
            print 'Checking name {}...'.format(login)
        if self.request.get('sigbtn'):
            print 'Registering user...'
            user = User()
            user.name
        if self.request.get('logbtn'):
            print 'Logging user...'


app = webapp2.WSGIApplication([
                                  ('/', MainHandler),
                                  ('/login', MainHandler),
                                  ('/checkname', MainHandler),
], debug=True, config = app_config)
