from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Volunteer, Organization


class LoginForm(FlaskForm):
    official_email = StringField('official_email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    org_name = StringField('name', validators=[DataRequired()])
    official_email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # def validate_username(self, name):
    #     volunteer = Volunteer.query.filter_by(name=name.data).first()
    #     if volunteer is not None:
    #         raise ValidationError('Please use a different name.')

    def validate_email(self, email):
        volunteer = Volunteer.query.filter_by(email=email.data).first()
        if volunteer is not None:
            raise ValidationError('Please use a different email address.')