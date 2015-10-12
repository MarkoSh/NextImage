# -*- coding: utf-8 -*-

import logging

import webapp2
import jinja2
from webapp2_extras import auth, sessions
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError

from app.lib.models.Users import User
from app.frypic.UserHandler import UserRequestHandler, ProfileHandler


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

app_config = {
        'webapp2_extras.auth': {
            'user_model': User,
            'user_attributes': ['name']
        },
        'webapp2_extras.sessions': {
            'secret_key': 'mimimimimimimimi'
        }
    }

ERRORMSG_TRYLOGIN = "May be you can try log in instead?"
ERRORMSG_INVLOGIN = "Ouch, you may be wrong"


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
        template_values = {
                'title': 'Login page',
                'login': False
            }
        if auth.get_auth().get_user_by_session():
            user_id = auth.get_auth().get_user_by_session()['user_id']
            user = User.get_by_id(user_id)
            userURI = user.name if user.name else user_id
            name = user.name if user.name else user.email_address
            if user:
                template_values = {
                    'title': 'Hi there, {}'.format(name),
                    'login': True,
                    'name': userURI,
                    'messages': ''
                }
            if self.request.path == '/':
                self.redirect('/{}'.format(user_id))
            if self.request.path == '/logout':
                auth.get_auth().unset_session()
                self.redirect('/')
                logging.info('Logout bye bye...')
            if self.request.path == '/profile':
                template_values['page'] = 'profile'
                profile = ProfileHandler()
                profile.drawProfilePage()
        template = JINJA_ENVIRONMENT.get_template('_layout.html')
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
                logging.info('Checking name {}...'.format(login))
                # TODO проверка доступности логина, вернуть джисоном результат
            if self.request.get('sigbtn'):
                logging.info('Registering user {}...'.format(login))
                if "@" in login and len(password) > 6:
                    unique_properties = ['email_address']
                    user = User.create_user(login, unique_properties,
                                            email_address=login,
                                            password_raw=password,
                                            verified=False)
                    if not user[0]:
                        template_values = {
                            'title': ERRORMSG_TRYLOGIN,
                            'notify': ERRORMSG_TRYLOGIN,
                            'login': False
                        }
                        logging.info('Unable to create user {}, duplicating key {}'.format(login, user[1]))
                    else:
                        logging.info('6sfull creating user {}'.format(login))
                        user_id = user[1].get_id()
                        auth.get_auth().set_session(auth.get_auth().store.user_to_dict(user[1]))
                        self.redirect('/{}'.format(user_id))
            if self.request.get('logbtn'):
                logging.info('Logging as {}...'.format(login))
                try:
                    user_id = auth.get_auth().get_user_by_password(login, password, remember=True, save_session=True,
                                                                   silent=False)['user_id']
                    self.session_store.save_sessions(self.response)
                    logging.info('6sfull logged user {} '.format(login))
                    self.redirect('/{}'.format(user_id))
                except (InvalidPasswordError, InvalidAuthIdError) as e:
                    template_values = {
                            'title': ERRORMSG_INVLOGIN,
                            'notify': ERRORMSG_INVLOGIN,
                            'login': False
                        }
                    logging.info("Auth error {}".format(type(e)))
            template = JINJA_ENVIRONMENT.get_template('_layout.html')
            self.response.write(template.render(template_values))



app = webapp2.WSGIApplication([
                                  ('/', MainHandler),
                                  # TODO сделать отдельный обработчик для страниц пользователей, в будущем возможны не только цифровые идентификаторы
                                  ('/login', MainHandler),
                                  ('/logout', MainHandler),
                                  ('/checkname', MainHandler),
                                  ('/feed', MainHandler),  # FeedHandler - обрабатываем ленту сети
                                  ('/video', MainHandler),  # FeedHandler - обрабатываем только медийную ленту
                                  ('/audio', MainHandler),  # FeedHandler - --//--
                                  ('/im', MainHandler),  # ImHandler - обрабатываем сообщеня
                                  ('/profile', MainHandler),  # ProfileHandler - обрабатываем профиль пользователя
                                  ('/settings', MainHandler),  # ProfileHandler - --//--
                                  ('/profile', MainHandler),  # ProfileHandler - --//--
                                  ('/\d+', MainHandler),  # идентификатор пользователя
                                  ('/g\d+', MainHandler),  # идентификатор группы
                                  #TODO сделать комплект обработчиков сервисных страниц
], debug=True, config = app_config)