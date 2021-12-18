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


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class RepairPeriod(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    loco_model = db.Column(db.String(10), nullable=False, index=True, unique=True)
    m3 = db.Column(db.Integer, nullable=False)
    cr1 = db.Column(db.Integer, nullable=False)
    cr2 = db.Column(db.Integer, nullable=False)
    cr3 = db.Column(db.Integer, nullable=False)
    mr = db.Column(db.Integer, nullable=False)
    overhaul = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<{self.loco_model}:ТО3 {self.m3},ТР1 {self.cr1},ТР2 {self.cr2},ТР3 {self.cr3},СР {self.mr},КР {self.overhaul}>'

