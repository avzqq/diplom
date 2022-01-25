from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, LocomotiveRepairPeriod, SavedRepairForms
from datetime import date, datetime, timedelta
from datetime import date, datetime
from config import ROWS_PER_PAGE


@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
@login_required
def index():
    page = request.args.get("page", 1, type=int)

    all_data = SavedRepairForms.query.paginate(
        page=page, per_page=ROWS_PER_PAGE)
    return render_template("index.html", forms=all_data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Некорректный логин или пароль.', "error")
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
        flash('Поздравляю, Вы зарегистрированы!', "success")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


def check_value(value):
    try:
        value = abs(int(value))
    except ValueError:
        flash("Количество дней должно быть целым числом.", "error")
        value = 0
    if value == 0:
        flash("Период проведения ремонта не может быть равен нулю.", "error")
    return value


@app.route('/create_model_record', methods=['POST'])
def create_model_record():
    if request.method == "POST":
        loco_model_name = request.form["loco_model_name"]
        three_maintenance = request.form["three_maintenance"]
        one_current_repair = request.form["one_current_repair"]
        two_current_repair = request.form["two_current_repair"]
        three_current_repair = request.form["three_current_repair"]
        medium_repair = request.form["medium_repair"]
        overhaul = request.form["overhaul"]

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
        if error:
            flash(error, "error")

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
        if len(request.form) == filled_fields:
            is_recordable = True
        else:
            is_recordable = False

        if is_recordable:
            db.session.add(new_model)
            db.session.commit()
            flash(f"Модель {new_model.loco_model_name} успешно добавлена.",
                  "success")
        else:
            flash("Ошибка записи: недопустимое значение поля.",
                 "error")

        return redirect(url_for("loco_model_table"))


@app.route('/edit_model_record', methods=['GET', 'POST'])
def edit_model_record():
    if request.method == "POST":
        record_id = request.form["record_id"]
        loco_model_name = request.form["loco_model_name"]
        three_maintenance = request.form["three_maintenance"]
        one_current_repair = request.form["one_current_repair"]
        two_current_repair = request.form["two_current_repair"]
        three_current_repair = request.form["three_current_repair"]
        medium_repair = request.form["medium_repair"]
        overhaul = request.form["overhaul"]

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
            if error:
                flash(error, "error")

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
            flash(f"Корректно заполненные поля были перезаписаны.", "success")

        return redirect(url_for("loco_model_table"))


@app.route('/delete_model_record/<id>/', methods=['GET', 'POST'])
def delete__model_record(id):
    record = LocomotiveRepairPeriod.query.get(id)
    db.session.delete(record)
    db.session.commit()
    flash(f"Модель {record.loco_model_name} удалена.", "success")
    
    return redirect(url_for("loco_model_table"))

  
@app.route('/create_repair_form', methods=['POST'])
def create_repair_form():

    try:
        loco_number = int(request.form["loco_number"])
    except ValueError:
        flash('Номер модели тепловоза должен быть числовым.', "error")
        return redirect(url_for("index"))

    loco_model_id = request.form.get("loco_model_id")
    last_three_maintenance = request.form.get("last_three_maintenance")
    next_three_maintenance = request.form.get("next_three_maintenance")
    last_three_current_repair = request.form.get("last_three_current_repair")
    next_three_current_repair = request.form.get("next_three_current_repair")
    last_two_current_repair = request.form.get("last_two_current_repair")
    next_two_current_repair = request.form.get("next_two_current_repair")
    last_one_current_repair = request.form.get("last_one_current_repair")
    next_one_current_repair = request.form.get("next_one_current_repair")
    last_medium_repair = request.form.get("last_medium_repair")
    next_medium_repair = request.form.get("next_medium_repair")
    last_overhaul = request.form.get("last_overhaul")
    next_overhaul = request.form.get("next_overhaul")
    notes = request.form.get("notes")
    timestamp = request.form.get("timestamp")

    try:
        loco_model_id = LocomotiveRepairPeriod.query.filter_by(
            loco_model_name=loco_model_id.strip()).first().id
    except AttributeError:
        loco_model_id = 0

    loco_model = LocomotiveRepairPeriod.query.get(loco_model_id)
    if not loco_model:
        flash('Такой модели не существует.', 'error')
        return redirect(url_for("index"))

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
        new_repair_form.last_overhaul = datetime.strptime(last_overhaul, '%Y-%m-%d')
        new_repair_form.next_overhaul = new_repair_form.last_overhaul + timedelta(loco_model.overhaul)
        new_repair_form.next_medium_repair = new_repair_form.last_overhaul + timedelta(loco_model.medium_repair)
        new_repair_form.next_three_current_repair = new_repair_form.last_overhaul + timedelta(loco_model.three_current_repair)
        new_repair_form.next_two_current_repair = new_repair_form.last_overhaul + timedelta(loco_model.two_current_repair)
        new_repair_form.next_one_current_repair = new_repair_form.last_overhaul + timedelta(loco_model.one_current_repair)
        new_repair_form.next_three_maintenance = new_repair_form.last_overhaul + timedelta(loco_model.three_maintenance)

    if last_medium_repair:
        new_repair_form.last_medium_repair = datetime.strptime(last_medium_repair, '%Y-%m-%d')
        new_repair_form.next_medium_repair = new_repair_form.last_medium_repair + timedelta(loco_model.medium_repair)
        new_repair_form.next_three_current_repair = new_repair_form.last_medium_repair + timedelta(loco_model.three_current_repair)
        new_repair_form.next_two_current_repair = new_repair_form.last_medium_repair + timedelta(loco_model.two_current_repair)
        new_repair_form.next_one_current_repair = new_repair_form.last_medium_repair + timedelta(loco_model.one_current_repair)
        new_repair_form.next_three_maintenance = new_repair_form.last_medium_repair + timedelta(loco_model.three_maintenance)

    if last_three_current_repair:
        new_repair_form.last_three_current_repair = datetime.strptime(last_three_current_repair, '%Y-%m-%d')
        new_repair_form.next_three_current_repair = new_repair_form.last_three_current_repair + timedelta(loco_model.three_current_repair)
        new_repair_form.next_two_current_repair = new_repair_form.last_three_current_repair + timedelta(loco_model.two_current_repair)
        new_repair_form.next_one_current_repair = new_repair_form.last_three_current_repair + timedelta(loco_model.one_current_repair)
        new_repair_form.next_three_maintenance = new_repair_form.last_three_current_repair + timedelta(loco_model.three_maintenance)

    if last_two_current_repair:
        new_repair_form.last_two_current_repair = datetime.strptime(last_two_current_repair, '%Y-%m-%d')
        new_repair_form.next_two_current_repair = new_repair_form.last_two_current_repair + timedelta(loco_model.two_current_repair)
        new_repair_form.next_one_current_repair = new_repair_form.last_two_current_repair + timedelta(loco_model.one_current_repair)
        new_repair_form.next_three_maintenance = new_repair_form.last_two_current_repair + timedelta(loco_model.three_maintenance)

    if last_one_current_repair:
        new_repair_form.last_one_current_repair = datetime.strptime(last_one_current_repair, '%Y-%m-%d')
        new_repair_form.next_one_current_repair = new_repair_form.last_one_current_repair + timedelta(loco_model.one_current_repair)
        new_repair_form.next_three_maintenance = new_repair_form.last_one_current_repair + timedelta(loco_model.three_maintenance)

    if last_three_maintenance:
        new_repair_form.last_three_maintenance = datetime.strptime(last_three_maintenance, '%Y-%m-%d')
        new_repair_form.next_three_maintenance = new_repair_form.last_three_maintenance + timedelta(loco_model.three_maintenance)

    if new_repair_form.query.filter_by(loco_number=loco_number).first():
        flash('Форма для этого тепловоза уже создана.', 'error')
        return redirect(url_for("index"))
    else:
        db.session.add(new_repair_form)
        db.session.commit()
        flash(f'Форма для тепловоза {loco_model_id} {loco_number} создана.',
              "success")
    return redirect(url_for("index"))


@app.route('/edit_repair_form', methods=['POST'])
def edit_repair_form():

    try:
        loco_number = int(request.form["loco_number"])
    except ValueError:
        flash('Номер модели тепловоза должен быть числовым.', 'error')
        return redirect(url_for("index"))

    repair_form_id = request.form.get("repair_form_id")
    loco_model_id = request.form.get("loco_model_id")
    last_three_maintenance = request.form.get("last_three_maintenance")
    last_three_current_repair = request.form.get("last_three_current_repair")
    last_two_current_repair = request.form.get("last_two_current_repair")
    last_one_current_repair = request.form.get("last_one_current_repair")
    last_medium_repair = request.form.get("last_medium_repair")
    last_overhaul = request.form.get("last_overhaul")
    notes = request.form.get("notes")
    timestamp = request.form.get("timestamp")

    old_form = SavedRepairForms.query.filter_by(id=repair_form_id).first_or_404()
    old_form.notes = notes

    loco_model = LocomotiveRepairPeriod.query.get(loco_model_id)
    if not loco_model:
        flash("Такой модели не существует.", "error")
        return redirect(url_for("index"))

    if loco_number != old_form.loco_number:
        if SavedRepairForms.query.filter_by(loco_number=loco_number).first():
            flash(f'Форма для тепловоза {loco_number} уже существует.',
                  "error")
            return redirect(url_for("index"))
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

    if last_medium_repair:
        old_form.last_medium_repair = datetime.strptime(last_medium_repair, '%d/%m/%Y')
        old_form.next_medium_repair = old_form.last_medium_repair + timedelta(loco_model.medium_repair)
        old_form.next_three_current_repair = old_form.last_medium_repair + timedelta(loco_model.three_current_repair)
        old_form.next_two_current_repair = old_form.last_medium_repair + timedelta(loco_model.two_current_repair)
        old_form.next_one_current_repair = old_form.last_medium_repair + timedelta(loco_model.one_current_repair)
        old_form.next_three_maintenance = old_form.last_medium_repair + timedelta(loco_model.three_maintenance)

    if last_three_current_repair:
        old_form.last_three_current_repair = datetime.strptime(last_three_current_repair, '%d/%m/%Y')
        old_form.next_three_current_repair = old_form.last_three_current_repair + timedelta(loco_model.three_current_repair)
        old_form.next_two_current_repair = old_form.last_three_current_repair + timedelta(loco_model.two_current_repair)
        old_form.next_one_current_repair = old_form.last_three_current_repair + timedelta(loco_model.one_current_repair)
        old_form.next_three_maintenance = old_form.last_three_current_repair + timedelta(loco_model.three_maintenance)

    if last_two_current_repair:
        old_form.last_two_current_repair = datetime.strptime(last_two_current_repair, '%d/%m/%Y')
        old_form.next_two_current_repair = old_form.last_two_current_repair + timedelta(loco_model.two_current_repair)
        old_form.next_one_current_repair = old_form.last_two_current_repair + timedelta(loco_model.one_current_repair)
        old_form.next_three_maintenance = old_form.last_two_current_repair + timedelta(loco_model.three_maintenance)

    if last_one_current_repair:
        old_form.last_one_current_repair = datetime.strptime(last_one_current_repair, '%d/%m/%Y')
        old_form.next_one_current_repair = old_form.last_one_current_repair + timedelta(loco_model.one_current_repair)
        old_form.next_three_maintenance = old_form.last_one_current_repair + timedelta(loco_model.three_maintenance)

    if last_three_maintenance:
        old_form.last_three_maintenance = datetime.strptime(last_three_maintenance, '%d/%m/%Y')
        old_form.next_three_maintenance = old_form.last_three_maintenance + timedelta(loco_model.three_maintenance)

    db.session.commit()

    flash("Запись изменена.", "success")
    return redirect(url_for("index"))


@app.route('/delete_repair_form/<id>/', methods=['GET', 'POST'])
def delete_repair_form(id):
    repair_form = SavedRepairForms.query.get(id) 
    db.session.delete(repair_form)
    db.session.commit()
    flash("Форма удалена", "success")

    return redirect(url_for("index"))
  

@app.route("/loco_model_table", methods=["GET", "POST"])
def loco_model_table():
    page = request.args.get("page", 1, type=int)

    all_data = LocomotiveRepairPeriod.query.paginate(
        page=page, per_page=ROWS_PER_PAGE)
    return render_template("loco_model_page.html", models=all_data)
