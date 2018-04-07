# -*- coding: utf-8 -*-
## Модуль обработчиков маршрутов приложений
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse

from app import app
from app.forms import LoginForm, EditProfileForm, AddTaskForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Task
from app import db
from app.forms import RegistrationForm
from datetime import datetime


@app.route('/')
@app.route('/index')
def index():
    """!
    Обработчик маршрута главной страницы (index).

    @return Страницу index.html с заголовком Home
    """
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """!
    Обработчик маршрута страницы входа (login).

    @return Страницу login.html с заголовком Войти, если логин/пароль были найдены.
    В противном случае выдает сообщение об ошибке.
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильный логин или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Войти', form=form)


@app.route('/logout')
def logout():
    """!
    Обработчик маршрута страницы выхода из системы (logout).

    @return Страницу index.html.
    """
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """!
    Обработчик маршрута страницы регистрации (register).

    @return Страницу login.html, если введенные логин/пароль валидны.
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, вы успешно зарегистрировались!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    """!
    Обработчик маршрута страницы личного кабинета пользователя (/user/<username>).

    @param username - имя пользователя
    @return Страницу user.html.
    """
    user = User.query.filter_by(username=username).first_or_404()
    tasks = Task.query.filter_by(user_id=user.id)

    return render_template('user.html', user=user, tasks=tasks)


@app.before_request
def before_request():
    """! Определение последнего посещения сайта пользователем."""
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """!
    Обработчик маршрута страницы редактирования профиля пользователя (edit_profile).

    @return Страницу edit_profile.html.
    """
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Изменения были сохранены.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Редактирование профиля',
                           form=form)


@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    """!
    Обработчик маршрута страницы добавления активности/задачи пользователя (edit_profile).

    @return Страницу add_task.html.
    """
    form = AddTaskForm()
    if form.validate_on_submit():
        task = form.task.data
        description = form.description.data
        start = datetime.utcnow()
        user_id = current_user.id

        t = Task.query.filter_by(task=task).first()
        if t is not None:
            flash('Такая задача уже существует')
            return redirect(url_for('add_task'))

        db.session.add(Task(task=task, description=description, start=start, user_id=user_id))
        db.session.commit()
        return redirect(url_for('user', username=current_user.username))
    return render_template('add_task.html', title='Добавить задачу', form=form)
