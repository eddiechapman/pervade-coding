from flask_wtf import FlaskForm
from flask import current_app
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    """Authentication form for registered users.

    Attributes:
        username: A field to enter a user's name.
        password: A field to enter a user's password.
        remember_me: Will the user be asked to log in next time?
        submit: A button to submit the form data.
        
    Raises:
        ValidationError: when the username or password field are left blank.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """Form fields for creating a user account.

    Attributes:
        username: A field to enter a user's name.
        email: A field to enter a user's email.
        password: A field to enter a user's password.
        password2: A field to confirm the user's password.
        submit: A button to submit the form data.

    Raises:
        ValidationError: When any fields are left blank at submit.
        ValidationError: When the email field does not conform to email format.
        ValidationError: When password and password2 do not match.
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """Check that there is no existing account with the submitted username.
        
        Args:
            username: The username field of the registration form.
            
        Raises:
            ValidationError: When the submitted username matches an existing account.
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """Check that the submitted email is valid.
        
        Check that there is no existing account with the submitted email.
        Also check that the email is listed in the config file.
        
        Args:
            email: The email field of the registration form.
            
        Raises:
            ValidationError: When the submitted email has already been claimed.
                Or, When the submitted email is not listed in config.
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        elif email.data not in current_app.config['PERVADE_MEMBER']:
            raise ValidationError(
                'You are not authorized to register. Try a different email address.'
            )


class ResetPasswordRequestForm(FlaskForm):
    """A form for requesting an email to reset a password.
    
    Attributes:
        email: A form for entering an email to receive a password reset link.
        submit: A button to submit the form data.
        
    Raises:
        ValidationError: When the form is submitted without an email value
        ValidationError: When the email value does not conform to an email format.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request password reset')


class ResetPasswordForm(FlaskForm):
    """A form for resetting a password once the reset email has been received.
    
    Attributes:
        password: A field for entering a user's new password.
        password2: A field for re-entering a user's new password.
        submit: A button to submit the form data.
        
    Raises:
        ValidationError: When either fields are left blank.
        ValidationError: When password and password2 do not match.
    """
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')