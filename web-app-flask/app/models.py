## Пакет классов моделей
#
# Пакет содержит классы, реализующие основные модели приложения:
# Пользователь, Задача

from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

## Класс пользователей
#
# @param UserMixin - класс, который включает в себя общие реализации классов пользовательских моделей
# @param db.Model - класс моделей SQLAlchemy
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    tasks = db.relationship('Task', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    ##  Представление объекта User при печати.
    def __repr__(self):
        return '<User {}>'.format(self.username)

    ##  Установка пароля.
    #
    # @param password - пароль
    # На основе пароля создается хэш, который и хранится
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    ##  Проверка пароля
    #
    # @param password - пароль
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    ##  Установка аватара.
    #
    # @param size - размер аватара.
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


##  Загрузка Пользователя
#
# @param id - первичный ключ пользователя
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

##Класс активностей
#
# @param db.Model - класс моделей SQLAlchemy
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(128))
    start = db.Column(db.DateTime, index=True)
    stop = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    ##  Представление объекта Task при печати.
    def __repr__(self):
        return '<Task {}>'.format(self.task)


