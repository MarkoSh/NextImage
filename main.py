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
        print self.request.path


app = webapp2.WSGIApplication([
                                  ('/', MainHandler),
                                  ('/login', MainHandler),
                                  ('/checkname', MainHandler),
], debug=True, config = app_config)
