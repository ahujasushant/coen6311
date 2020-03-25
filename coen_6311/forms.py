from flask_wtf import FlaskForm
from wtforms  import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from coen_6311.models import Volunteer, Organization, Post


class LoginForm(FlaskForm):
    official_email = StringField('Official Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    org_name = StringField('Organization Name', validators=[DataRequired()])
    official_email = StringField('Official Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register ')

    def validate_email(self, email):
        organization = Organization.query.filter_by(email=email.data).first()
        if organization is not None:
            raise ValidationError('Please use a different email address.')


class VolunteerLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class PostForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Create Post')


class VolunteerRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        volunteer = Volunteer.query.filter_by(email=email.data).first()
        if volunteer is not None:
            raise ValidationError('Please use a different email address.')