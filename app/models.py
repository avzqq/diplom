from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class DataStore(db.Model):
    '''
    m = maintenance = ТО
    cr = current repair = текущий ремонт
    mr = medium repair = средний ремонт
    overhaul = капитальный ремонт'''

    id = db.Column(db.Integer, primary_key=True)

    loco_model = db.Column(db.String(10), nullable=False)
    loco_number = db.Column(db.String(10), nullable=False)

    m3_last = db.Column(db.Date)
    m3_next = db.Column(db.Date)

    cr1_last = db.Column(db.Date)
    cr1_next = db.Column(db.Date)
    
    cr2_last = db.Column(db.Date)
    cr2_next = db.Column(db.Date)

    cr3_last = db.Column(db.Date)
    cr3_next = db.Column(db.Date)
    
    mr_last = db.Column(db.Date)
    mr_next = db.Column(db.Date)
    
    overhaul_last = db.Column(db.Date)
    overhaul_next = db.Column(db.Date)

    notes = db.Column(db.Text)


    def __repr__(self):
        return f'<Storage table for locomotive {self.loco_model} {self.loco_number}>'



@login.user_loader
def load_user(id):
    return User.query.get(int(id))
