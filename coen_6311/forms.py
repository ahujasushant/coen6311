from flask_wtf import FlaskForm
from wtforms  import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from coen_6311.models import Volunteer, Organization


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
        organization = Organization.query.filter_by(email=email.data).first()
        if organization is not None:
            raise ValidationError('Please use a different email address.')


class VolunteerLoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class VolunteerRegistrationForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        volunteer = Volunteer.query.filter_by(email=email.data).first()
        if volunteer is not None:
            raise ValidationError('Please use a different email address.')