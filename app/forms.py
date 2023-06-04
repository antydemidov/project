# from flask_login import user_accessed
from flask_wtf import FlaskForm
from wtforms import (PasswordField, SelectField, StringField,
                     SubmitField)
from wtforms.validators import DataRequired, EqualTo, Length


password_length = Length(6, message='Пароль должен содержать от 6 символов!')
data_required = DataRequired("Поле необходимо заполнить!")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           data_required])
    password1 = PasswordField('Password', validators=[
        data_required,
        password_length
    ])
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[data_required])
    password1 = PasswordField('Password',
                              validators=[data_required, password_length]
                              )
    password2 = PasswordField('Confirm Password',
                              validators=[
        data_required,
        EqualTo('password1', "Пароли не совпадают!"),
        password_length
    ])
    submit = SubmitField('Sign Up')


class SearchForm(FlaskForm):
    search = StringField('Search',
                         validators=[data_required],
                         default='Search',
                         render_kw={'class': 'btn btn-success btn-block'}
                         )
    submit = SubmitField('Search',
                         render_kw={'class': 'btn btn-success btn-block'}
                         )


class FilterForm(FlaskForm):
    field = SelectField('Select',
                        choices=['---', 'Actual', 'Not actual'],
                        render_kw={'class': 'btn btn-success btn-block'}
                        )
    submit = SubmitField('Select',
                         render_kw={'class': 'btn btn-success btn-block'}
                         )


class LengthSelector(FlaskForm):
    selector = SelectField('Select',
                           choices=[12, 24, 48, 96],
                           render_kw={'class': 'btn btn-success btn-block'}
                           )
