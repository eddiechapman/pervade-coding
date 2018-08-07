from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class CodingForm(FlaskForm):
    pervasive_data = BooleanField('Pervasive data')
    data_science = BooleanField('Data science')
    big_data = BooleanField('Big data')
    case_study = BooleanField('Flag for PRIM&R case study')
    data_synonyms = TextAreaField(
        'Data synonyms',
        description='Please seperate values with a semicolon',
        validators=[Length(min=0, max=500)]
    )
    not_relevant = BooleanField('This award is not relevant to PERVADE')
    submit = SubmitField('Submit')

    def validate(self):
        if not self.pervasive_data.data \
            and not self.data_science.data \
            and not self.big_data.data \
            and not self.case_study.data \
            and not self.data_synonyms.data \
            and not self.not_relevant.data:
            flash('Please select a coding category or NOT RELEVANT to proceed.')
            return False
        return True