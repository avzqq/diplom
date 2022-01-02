from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, SavedRepairForms
from datetime import date, datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Некорректный логин или пароль.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляю, Вы зарегистрированы!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/get_forms_list')
def get_forms_list():
    list_of_forms = []
    for form in SavedRepairForms.query:
        list_of_forms.append([
            form.loco_model_id,
            form.loco_number,
            form.last_three_maintenance,
            form.next_three_maintenance,
            form.last_three_current_repair,
            form.next_three_current_repair,
            form.last_two_current_repair,
            form.next_two_current_repair,
            form.last_one_current_repair,
            form.next_one_current_repair,
            form.last_medium_repair,
            form.next_medium_repair,
            form.last_overhaul,
            form.next_overhaul,
            form.notes,
            form.timestamp
            ])

    # make it pretty    
    for row in list_of_forms:
        for i in row:
             if type(i) == date:
                row[row.index(i)] = str(i)
             elif type(i) == datetime:
                 row[row.index(i)] = i.strftime("%Y-%m-%d %H:%M:%S")
             elif not bool(i):
                 row[row.index(i)] = ""
                 
    return str(list_of_forms)

