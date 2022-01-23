from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, LocomotiveRepairPeriod, SavedRepairForms
from datetime import date, datetime, timedelta


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


def check_value(value):
    try:
        value = abs(int(value))
    except ValueError:
        flash(f"{value}: количество дней должно быть целым числом.")
        value = 0

    return value


@app.route('/create_model_record', methods=['POST'])
def create_model_record():
    loco_model_name = request.json.get("loco_model_name")
    three_maintenance = request.json.get("three_maintenance")
    one_current_repair = request.json.get("one_current_repair")
    two_current_repair = request.json.get("two_current_repair")
    three_current_repair = request.json.get("three_current_repair")
    medium_repair = request.json.get("medium_repair")
    overhaul = request.json.get("overhaul")

    filled_fields = 0
    error = None
    new_model = LocomotiveRepairPeriod()
    if new_model.query.filter_by(loco_model_name=loco_model_name).first():
        error = f"Для модели {loco_model_name} запись уже существует."
    elif loco_model_name == '':
        error = "Необходимо указать модель"
    elif not isinstance(loco_model_name, str):
        error = "Название модели должно быть строкой!"
    else:
        new_model.loco_model_name = loco_model_name
        filled_fields += 1
    flash(error)

    validator = check_value(three_maintenance)
    if validator:
        new_model.three_maintenance = validator
        filled_fields += 1

    validator = check_value(one_current_repair)
    if validator:
        new_model.one_current_repair = validator
        filled_fields += 1

    validator = check_value(two_current_repair)
    if validator:
        new_model.two_current_repair = validator
        filled_fields += 1

    validator = check_value(three_current_repair)
    if validator:
        new_model.three_current_repair = validator
        filled_fields += 1

    validator = check_value(medium_repair)
    if validator:
        new_model.medium_repair = validator
        filled_fields += 1

    validator = check_value(overhaul)
    if validator:
        new_model.overhaul = validator
        filled_fields += 1

    if len(list(request.json.values())) == filled_fields:
        is_recordable = True
    else:
        is_recordable = False

    if is_recordable:
        db.session.add(new_model)
        db.session.commit()
    else:
        flash("Ошибка записи: одно из полей имеет недопустимое значение.")

    return "Когда-нибудь здесь что-то появится."


@app.route('/edit_model_record', methods=['POST'])
def edit_model_record():
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
    table = LocomotiveRepairPeriod
    old_model = table.query.filter_by(id=record_id).first_or_404()

    if loco_model_name != old_model.loco_model_name:
        if table.query.filter_by(loco_model_name=loco_model_name).first():
            error = f"Для модели {loco_model_name} запись уже существует."
            is_recordable = False
        elif loco_model_name == '':
            error = "Необходимо указать модель"
        elif not isinstance(loco_model_name, str):
            error = "Название модели должно быть строкой!"
        else:
            old_model.loco_model_name = loco_model_name
        flash(error)

    validator = check_value(three_maintenance)
    if validator:
        old_model.three_maintenance = validator

    validator = check_value(one_current_repair)
    if validator:
        old_model.one_current_repair = validator

    validator = check_value(two_current_repair)
    if validator:
        old_model.two_current_repair = validator

    validator = check_value(three_current_repair)
    if validator:
        old_model.three_current_repair = validator

    validator = check_value(medium_repair)
    if validator:
        old_model.medium_repair = validator

    validator = check_value(overhaul)
    if validator:
        old_model.overhaul = validator

    if is_recordable:
        db.session.commit()

    return "Когда-нибудь здесь что-то появится."


@app.route('/delete_model_record', methods=['POST'])
def delete_model_record():
    record_id = request.json.get("record_id")
    model = LocomotiveRepairPeriod.query.filter_by(id=record_id).first_or_404()
    db.session.delete(model)
    db.session.commit()

    return f"Модель {model.loco_model_name} удалена."


@app.route('/get_models_list')
def get_models_list():
    list_of_models = []
    for instance in LocomotiveRepairPeriod.query:
        list_of_models.append([
            instance.loco_model_name,
            instance.three_maintenance,
            instance.one_current_repair,
            instance.two_current_repair,
            instance.three_current_repair,
            instance.medium_repair,
            instance.overhaul
            ])

    return str(list_of_models)


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


@app.route('/create_repair_form', methods=['POST'])
def create_repair_form():

    try:
        loco_number = int(request.form["loco_number"])
    except ValueError:
        return {'Error': 'Номер модели тепловоза должен быть числовым.'}

    loco_model_id = request.form["loco_model_id"]
    last_three_maintenance = request.form["last_three_maintenance"]
    next_three_maintenance = request.form["next_three_maintenance"]
    last_three_current_repair = request.form["last_three_current_repair"]
    next_three_current_repair = request.form["next_three_current_repair"]
    last_two_current_repair = request.form["last_two_current_repair"]
    next_two_current_repair = request.form["next_two_current_repair"]
    last_one_current_repair = request.form["last_one_current_repair"]
    next_one_current_repair = request.form["next_one_current_repair"]
    last_medium_repair = request.form["last_medium_repair"]
    next_medium_repair = request.form["next_medium_repair"]
    last_overhaul = request.form["last_overhaul"]
    next_overhaul = request.form["next_overhaul"]
    notes = request.form["notes"]
    timestamp = request.form["timestamp"]

    loco_model = LocomotiveRepairPeriod.query.get(loco_model_id)
    if not loco_model:
        return {'Error': 'такой модели не существует.'}

    new_repair_form = SavedRepairForms(
            loco_model_id=loco_model_id,
            loco_number=loco_number,
            notes=notes
        )

    try:
        new_repair_form.notes = notes
    except TypeError:
        pass

    if last_overhaul:
        new_repair_form.last_overhaul = datetime.strptime(last_overhaul, '%d/%m/%Y')
        new_repair_form.next_overhaul = new_repair_form.last_overhaul + timedelta(loco_model.overhaul)
        new_repair_form.next_medium_repair = new_repair_form.last_overhaul + timedelta(loco_model.medium_repair)
        new_repair_form.next_three_current_repair = new_repair_form.last_overhaul + timedelta(loco_model.three_current_repair)
        new_repair_form.next_two_current_repair = new_repair_form.last_overhaul + timedelta(loco_model.two_current_repair)
        new_repair_form.next_one_current_repair = new_repair_form.last_overhaul + timedelta(loco_model.one_current_repair)
        new_repair_form.next_three_maintenance = new_repair_form.last_overhaul + timedelta(loco_model.three_maintenance)
    else:
        pass

    if last_medium_repair:
        new_repair_form.last_medium_repair = datetime.strptime(last_medium_repair, '%d/%m/%Y')
        new_repair_form.next_medium_repair = new_repair_form.last_medium_repair + timedelta(loco_model.medium_repair)
        new_repair_form.next_three_current_repair = new_repair_form.last_medium_repair + timedelta(loco_model.three_current_repair)
        new_repair_form.next_two_current_repair = new_repair_form.last_medium_repair + timedelta(loco_model.two_current_repair)
        new_repair_form.next_one_current_repair = new_repair_form.last_medium_repair + timedelta(loco_model.one_current_repair)
        new_repair_form.next_three_maintenance = new_repair_form.last_medium_repair + timedelta(loco_model.three_maintenance)
    else:
        pass

    if last_three_current_repair:
        new_repair_form.last_three_current_repair = datetime.strptime(last_three_current_repair, '%d/%m/%Y')
        new_repair_form.next_three_current_repair = new_repair_form.last_three_current_repair + timedelta(loco_model.three_current_repair)
        new_repair_form.next_two_current_repair = new_repair_form.last_three_current_repair + timedelta(loco_model.two_current_repair)
        new_repair_form.next_one_current_repair = new_repair_form.last_three_current_repair + timedelta(loco_model.one_current_repair)
        new_repair_form.next_three_maintenance = new_repair_form.last_three_current_repair + timedelta(loco_model.three_maintenance)
    else:
        pass

    if last_two_current_repair:
        new_repair_form.last_two_current_repair = datetime.strptime(last_two_current_repair, '%d/%m/%Y')
        new_repair_form.next_two_current_repair = new_repair_form.last_two_current_repair + timedelta(loco_model.two_current_repair)
        new_repair_form.next_one_current_repair = new_repair_form.last_two_current_repair + timedelta(loco_model.one_current_repair)
        new_repair_form.next_three_maintenance = new_repair_form.last_two_current_repair + timedelta(loco_model.three_maintenance)
    else:
        pass

    if last_one_current_repair:
        new_repair_form.last_one_current_repair = datetime.strptime(last_one_current_repair, '%d/%m/%Y')
        new_repair_form.next_one_current_repair = new_repair_form.last_one_current_repair + timedelta(loco_model.one_current_repair)
        new_repair_form.next_three_maintenance = new_repair_form.last_one_current_repair + timedelta(loco_model.three_maintenance)
    else:
        pass

    if last_three_maintenance:
        new_repair_form.last_three_maintenance = datetime.strptime(last_three_maintenance, '%d/%m/%Y')
        new_repair_form.next_three_maintenance = new_repair_form.last_three_maintenance + timedelta(loco_model.three_maintenance)
    else:
        pass

    if new_repair_form.query.filter_by(loco_number=loco_number).first():
        return {'error': 'Форма для этого тепловоза уже создана.'}
    else:
        db.session.add(new_repair_form)
        db.session.commit()

    return f'Форма для тепловоза {loco_model_id} {loco_number} создана.'


@app.route('/edit_repair_form', methods=['POST'])
def edit_repair_form():

    try:
        loco_number = int(request.json.get("loco_number"))
    except ValueError:
        return {'Error': 'Номер модели тепловоза должен быть числовым.'}

    repair_form_id = request.form["repair_form_id"]
    loco_model_id = request.form["loco_model_id"]
    last_three_maintenance = request.form["last_three_maintenance"]
    last_three_current_repair = request.form["last_three_current_repair"]
    last_two_current_repair = request.form["last_two_current_repair"]
    last_one_current_repair = request.form["last_one_current_repair"]
    last_medium_repair = request.form["last_medium_repair"]
    last_overhaul = request.form["last_overhaul"]
    notes = request.form["notes"]
    timestamp = request.form["timestamp"]

    old_form = SavedRepairForms.query.filter_by(id=repair_form_id).first_or_404()
    old_form.notes = notes

    loco_model = LocomotiveRepairPeriod.query.get(loco_model_id)
    if not loco_model:
        return {'Error': 'такой модели не существует.'}

    if loco_number != old_form.loco_number:
        if SavedRepairForms.query.filter_by(loco_number=loco_number).first():
            return f'Форма для тепловоза {loco_number} уже существует.'
        else:
            old_form.loco_number = loco_number

    if last_overhaul:
        old_form.last_overhaul = datetime.strptime(last_overhaul, '%d/%m/%Y')
        old_form.next_overhaul = old_form.last_overhaul + timedelta(loco_model.overhaul)
        old_form.next_medium_repair = old_form.last_overhaul + timedelta(loco_model.medium_repair)
        old_form.next_three_current_repair = old_form.last_overhaul + timedelta(loco_model.three_current_repair)
        old_form.next_two_current_repair = old_form.last_overhaul + timedelta(loco_model.two_current_repair)
        old_form.next_one_current_repair = old_form.last_overhaul + timedelta(loco_model.one_current_repair)
        old_form.next_three_maintenance = old_form.last_overhaul + timedelta(loco_model.three_maintenance)
    else:
        pass

    if last_medium_repair:
        old_form.last_medium_repair = datetime.strptime(last_medium_repair, '%d/%m/%Y')
        old_form.next_medium_repair = old_form.last_medium_repair + timedelta(loco_model.medium_repair)
        old_form.next_three_current_repair = old_form.last_medium_repair + timedelta(loco_model.three_current_repair)
        old_form.next_two_current_repair = old_form.last_medium_repair + timedelta(loco_model.two_current_repair)
        old_form.next_one_current_repair = old_form.last_medium_repair + timedelta(loco_model.one_current_repair)
        old_form.next_three_maintenance = old_form.last_medium_repair + timedelta(loco_model.three_maintenance)
    else:
        pass

    if last_three_current_repair:
        old_form.last_three_current_repair = datetime.strptime(last_three_current_repair, '%d/%m/%Y')
        old_form.next_three_current_repair = old_form.last_three_current_repair + timedelta(loco_model.three_current_repair)
        old_form.next_two_current_repair = old_form.last_three_current_repair + timedelta(loco_model.two_current_repair)
        old_form.next_one_current_repair = old_form.last_three_current_repair + timedelta(loco_model.one_current_repair)
        old_form.next_three_maintenance = old_form.last_three_current_repair + timedelta(loco_model.three_maintenance)
    else:
        pass

    if last_two_current_repair:
        old_form.last_two_current_repair = datetime.strptime(last_two_current_repair, '%d/%m/%Y')
        old_form.next_two_current_repair = old_form.last_two_current_repair + timedelta(loco_model.two_current_repair)
        old_form.next_one_current_repair = old_form.last_two_current_repair + timedelta(loco_model.one_current_repair)
        old_form.next_three_maintenance = old_form.last_two_current_repair + timedelta(loco_model.three_maintenance)
    else:
        pass

    if last_one_current_repair:
        old_form.last_one_current_repair = datetime.strptime(last_one_current_repair, '%d/%m/%Y')
        old_form.next_one_current_repair = old_form.last_one_current_repair + timedelta(loco_model.one_current_repair)
        old_form.next_three_maintenance = old_form.last_one_current_repair + timedelta(loco_model.three_maintenance)
    else:
        pass

    if last_three_maintenance:
        old_form.last_three_maintenance = datetime.strptime(last_three_maintenance, '%d/%m/%Y')
        old_form.next_three_maintenance = old_form.last_three_maintenance + timedelta(loco_model.three_maintenance)
    else:
        pass

    db.session.commit()

    return "запись изменена."

@app.route('/delete_repair_form', methods=['POST'])
def delete_repair_form():
    repair_form_id = request.form["repair_form_id"]
    repair_form = SavedRepairForms.query.filter_by(id=repair_form_id).first_or_404()
    db.session.delete(repair_form)
    db.session.commit()

    return f"Форма удалена."
