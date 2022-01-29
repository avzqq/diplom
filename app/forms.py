from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()],
                           render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()],
                           render_kw={"class": "form-control"})
    remember_me = BooleanField('Запомнить меня',
                            render_kw={"class": "form-check-label"})
    submit = SubmitField('Вход', render_kw={"class": "btn btn-primary"}) 


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()], 
                           render_kw={"class": "form-control"})
    email = StringField('Email', validators=[DataRequired(), Email()],
                            render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')],
                             render_kw={"class": "form-control"})
    submit = SubmitField('Регистрация', render_kw={"class": "btn btn-primary"})


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Используйте другой логин.')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Используйте другой email.')
