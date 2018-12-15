from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from app import app


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request password reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat passsword', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


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
        elif email.data not in app.config['PERVADE_MEMBER']:
            raise ValidationError(
                'You are not authorized to register. Try a different email address.'
            )


class CodingForm(FlaskForm):
    title_pervasive_data = BooleanField('Pervasive data (title)')
    title_data_science = BooleanField('Data science (title)')
    title_big_data = BooleanField('Big data (title)')
    title_case_study = BooleanField('Flag for PRIM&R case study (title)')
    title_data_synonyms = TextAreaField(
        'Data synonyms (title)',
        description='Please separate values with a semicolon',
        validators=[Length(min=0, max=500)]
    )
    abstract_pervasive_data = BooleanField('Pervasive data (abstract)')
    abstract_data_science = BooleanField('Data science (abstract)')
    abstract_big_data = BooleanField('Big data (abstract)')
    abstract_case_study = BooleanField('Flag for PRIM&R case study (abstract)')
    abstract_data_synonyms = TextAreaField(
        'Data synonyms (abstract)',
        description='Please separate values with a semicolon',
        validators=[Length(min=0, max=500)]
    )
    submit = SubmitField('Submit')


