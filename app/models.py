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

class LocomotiveRepairPeriod(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    loco_model_name = db.Column(db.String(10), nullable=False, index=True, unique=True)
    three_maintenance = db.Column(db.Integer, nullable=False)
    one_current_repair = db.Column(db.Integer, nullable=False)
    two_current_repair = db.Column(db.Integer, nullable=False)
    three_current_repair = db.Column(db.Integer, nullable=False)
    medium_repair = db.Column(db.Integer, nullable=False)
    overhaul = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<{self.loco_model_name}:' \
               f'ТО3 {self.three_maintenance}' \
               f'ТР1 {self.one_current_repair}' \
               f'ТР2 {self.two_current_repair}' \
               f'ТР3 {self.three_current_repair}' \
               f'СР {self.medium_repair}' \
               f'КР {self.overhaul}>'


