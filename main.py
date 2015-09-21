# -*- coding: utf-8 -*-
import os

import webapp2
import jinja2
from webapp2_extras import auth, sessions
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError

from models.Users import User


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
TEMPLATES_PATH = "tmpls/"

app_config = {
        'webapp2_extras.auth': {
            'user_model': User,
            'user_attributes': ['name']
        },
        'webapp2_extras.sessions': {
            'secret_key': 'mimimimimimimimi'
        }
    }

class MainHandler(webapp2.RequestHandler):
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
        template_values = {
                'title': 'Login page',
                'login': False
            }
        if auth.get_auth().get_user_by_session():
            user_id = auth.get_auth().get_user_by_session()['user_id']
            # self.redirect('/{}'.format(user_id))
            user = User.get_by_id(user_id)
            userURI = user.name if user.name else user_id
            name = user.name if user.name else user.email_address
            if user:
                template_values = {
                    'title': 'Hi there, {}'.format(name),
                    'login': True,
                    'name': userURI
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
                if "@" in login and len(password) > 6:
                    unique_properties = ['email_address']
                    user = User.create_user(login, unique_properties, email_address=login, password_raw=password,
                                            verified=False)
                    if not user[0]:
                        template_values = {
                            'title': 'May be you can try log in instead?',
                            'notify': 'May be you can try log in instead?',
                            'login': False
                        }
                        print 'Unable to create user {}, duplicating key {}'.format(login, user[1])
                    else:
                        template_values = {
                            'title': 'Now you can create everything',
                            'login': True
                        }
                        print '6sfull creating user {}'.format(login)
                        user_id = user[1].get_id()
                        self.session_store.save_sessions(self.response)
                        self.redirect('/{}'.format(user_id))


            if self.request.get('logbtn'):
                print 'Logging as {}...'.format(login)
                try:
                    user_id = auth.get_auth().get_user_by_password(login, password, remember=True, save_session=True,
                                                                   silent=False)['user_id']
                    self.session_store.save_sessions(self.response)
                    print '6sfull logged user {} '.format(login)
                    self.redirect('/{}'.format(user_id))
                except (InvalidPasswordError, InvalidAuthIdError) as e:
                    template_values = {
                            'title': 'Ouch, you may be wrong',
                            'notify': 'Ouch, you may be wrong',
                            'login': False
                        }
                    print "Auth error {}".format(type(e))
            template = JINJA_ENVIRONMENT.get_template(TEMPLATES_PATH + '_layout.html')
            self.response.write(template.render(template_values))



app = webapp2.WSGIApplication([
                                  ('/', MainHandler),
                                  ('/\d+', MainHandler),
                                  # TODO сделать отдельный обработчик для страниц пользователей, в будущем возможны не только цифровые идентификаторы
                                  ('/login', MainHandler),
                                  ('/logout', MainHandler),
                                  ('/checkname', MainHandler),
                                  #TODO сделать комплект обработчиков сервисных страниц
], debug=True, config = app_config)
