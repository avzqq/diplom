from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, LocomotiveRepairPeriod


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


@app.route('/create_model_record', methods=['POST'])
def create_model_record():
    loco_model_name = request.json.get("loco_model_name")
    three_maintenance = request.json.get("three_maintenance")
    one_current_repair = request.json.get("one_current_repair")
    two_current_repair = request.json.get("two_current_repair")
    three_current_repair = request.json.get("three_current_repair")
    medium_repair = request.json.get("medium_repair")
    overhaul = request.json.get("overhaul")
   
    error = None
    type_error = "Количество дней должно быть целым числом!"
    new_model = LocomotiveRepairPeriod()
    if LocomotiveRepairPeriod.query.filter_by(loco_model_name=loco_model_name).first():
        error = "Для модели {loco_model_name} запись уже существует."
    elif loco_model_name == '':
        error = "Необходимо указать модель"
    elif not isinstance(loco_model_name, str):
        error = "Название модели должно быть строкой!"
    else:
        new_model.loco_model_name = loco_model_name
    flash(error)

    if three_maintenance:
        if isinstance(three_maintenance, int):
            new_model.three_maintenance = abs(three_maintenance)
        else:
            flash(f"{three_maintenance}: {type_error}")

    if one_current_repair:
        if isinstance(one_current_repair, int):
            new_model.one_current_repair = abs(one_current_repair)
        else:
            flash(f"{one_current_repair}: {type_error}")

    if two_current_repair:
        if isinstance(two_current_repair, int):
            new_model.two_current_repair = abs(two_current_repair)
        else:
            flash(f"{two_current_repair}: {type_error}")

    if three_current_repair:
        if isinstance(three_current_repair, int):
            new_model.three_current_repair = abs(three_current_repair)
        else:
            flash(f"{three_current_repair}: {type_error}")

    if medium_repair:
        if isinstance(medium_repair, int):
            new_model.medium_repair = abs(medium_repair)
        else:
            flash(f"{medium_repair}: {type_error}")

    if overhaul:
        if isinstance(overhaul, int):
            new_model.overhaul = abs(overhaul)
        else:
            flash(f"{overhaul}: {type_error}")

    is_recordable = bool(new_model.loco_model_name and new_model.three_maintenance and 
                        new_model.one_current_repair and new_model.two_current_repair and 
                        new_model.three_current_repair and new_model.medium_repair and
                        new_model.overhaul
                        )
    if is_recordable:
        db.session.add(new_model)
        db.session.commit()
    else:
        flash("Ошибка записи в базу данных: одно из полей имеет недопустимое значение")

    return "Когда-нибудь здесь что-то появится."


@app.route('/edit_model_record', methods=['POST'])
def edit__model_record():
    record_id = request.json.get("record_id")
    loco_model_name = request.json.get("loco_model_name")
    three_maintenance = request.json.get("three_maintenance")
    one_current_repair = request.json.get("one_current_repair")
    two_current_repair = request.json.get("two_current_repair")
    three_current_repair = request.json.get("three_current_repair")
    medium_repair = request.json.get("medium_repair")
    overhaul = request.json.get("overhaul")
   
    is_recordable = True
    error = None
    type_error = "Количество дней должно быть целым числом!"
    old_model = LocomotiveRepairPeriod.query.filter_by(id=record_id).first_or_404()

    if loco_model_name != old_model.loco_model_name:
        if LocomotiveRepairPeriod.query.filter_by(loco_model_name=loco_model_name).first():
            error = "Для модели {loco_model_name} запись уже существует."
            is_recordable = False
        elif loco_model_name == '':
            error = "Необходимо указать модель"
        elif not isinstance(loco_model_name, str):
            error = "Название модели должно быть строкой!"
        else:
            old_model.loco_model_name = loco_model_name
        flash(error)

    if three_maintenance:
        if isinstance(three_maintenance, int):
            old_model.three_maintenance = abs(three_maintenance)
        else:
            flash(f"{three_maintenance}: {type_error}")

    if one_current_repair:
        if isinstance(one_current_repair, int):
            old_model.one_current_repair = abs(one_current_repair)
        else:
            flash(f"{one_current_repair}: {type_error}")

    if two_current_repair:
        if isinstance(two_current_repair, int):
            old_model.two_current_repair = abs(two_current_repair)
        else:
            flash(f"{two_current_repair}: {type_error}")

    if three_current_repair:
        if isinstance(three_current_repair, int):
            old_model.three_current_repair = abs(three_current_repair)
        else:
            flash(f"{three_current_repair}: {type_error}")

    if medium_repair:
        if isinstance(medium_repair, int):
            old_model.medium_repair = abs(medium_repair)
        else:
            flash(f"{medium_repair}: {type_error}")

    if overhaul:
        if isinstance(overhaul, int):
            old_model.overhaul = abs(overhaul)
        else:
            flash(f"{overhaul}: {type_error}")

    if is_recordable:
        db.session.commit()

    return "Когда-нибудь здесь что-то появится."


@app.route('/delete_model_record', methods=['POST'])
def delete__model_record():
    record_id = request.json.get("record_id")
    model = LocomotiveRepairPeriod.query.filter_by(id=record_id).first_or_404()
    db.session.delete(model)
    db.session.commit()

    return f"Модель {model.loco_model_name} удалена."






