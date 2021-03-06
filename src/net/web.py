from concurrent.futures import ThreadPoolExecutor

import bcrypt
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.web import RequestHandler

from db import torndb
from core.player import Player


class BaseHandler(RequestHandler):
    @property
    def db(self) -> torndb.Connection:
        return self.application.db

    @property
    def executor(self) -> ThreadPoolExecutor:
        return self.application.executor

    def data_received(self, chunk):
        pass

    # def on_finish(self):
        # self.session.flush()


class WebHandler(BaseHandler):
    # @tornado.web.authenticated
    def get(self):
        self.render('poker.html')


def auth_reg(self):
    email = self.get_argument('email')
    account = self.db.get('SELECT * FROM account WHERE email="%s"', email)
    if account:
        raise tornado.web.HTTPError(400, "email already taken")

    username = self.get_argument('username')
    password = self.get_argument('password')
    password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

    uid = self.db.insert('INSERT INTO account (email, username, password) VALUES ("%s", "%s", "%s")',
                         email, username, password)

    self.set_secure_cookie('uid', str(uid))
    self.session.save(uid, Player(uid, username=username))
    self.redirect(self.get_argument("next", "/"))


def auth_login(self):
    account = self.db.get('SELECT * FROM account WHERE email="%s"', self.get_argument('email'))
    password = self.get_argument("password")
    password = bcrypt.hashpw(password.encode('utf8'), account.get('password'))

    if password == account.get('password'):
        self.set_secure_cookie("uid", str(account.get('id')))
        self.redirect(self.get_argument("next", "/"))
        return True
    return False


def auth_logout(self):
    uid = self.get_secure_cookie("uid")
    self.clear_cookie("uid")
    self.session.remove(int(uid))
    self.redirect(self.get_argument("next", "/"))
