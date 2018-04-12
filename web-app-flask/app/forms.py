from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    """!
    Класс формы входа

    @param FlaskForm - родительский класс форм
    """
    username = StringField('Пользователь', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    """!
    Класс формы регистрации

    @param FlaskForm - родительский класс форм
    """
    username = StringField('Пользователь', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        """!
        Валидация имени пользователя.

        @param username - имя пользователя
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пользователь с таким именем уже существует.')

    def validate_email(self, email):
        """!
        Валидация адреса e-mail.

        @param email - электронная почта
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email адрес уже используется.')

"""
class EditProfileForm(FlaskForm):
    username = StringField('Пользователь', validators=[DataRequired()])
    about_me = TextAreaField('Обо мне', validators=[Length(min=0, max=140)])
    submit = SubmitField('Применить')
"""


class EditProfileForm(FlaskForm):
    """!
    Класс формы редактирования профиля

    @param FlaskForm - родительский класс форм
    """
    username = StringField('Пользователь', validators=[DataRequired()])
    about_me = TextAreaField('Обо мне', validators=[Length(min=0, max=140)])
    submit = SubmitField('Применить')

    def __init__(self, original_username, *args, **kwargs):
        """! Конструктор
        @param original_username - имя пользователя.
        """
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        """! алидация имени пользователя.

        @param username - имя пользователя """
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Данное имя пользователя уже занято.')


class AddTaskForm(FlaskForm):
    """!
    Класс формы добавления активности/задачи

    @param FlaskForm - родительский класс форм
    """
    task = StringField('Задача', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[Length(min=0, max=128)])
    submit = SubmitField('Применить')
