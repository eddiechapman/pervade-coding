from flask import render_template, current_app
from app.email import send_email


def send_password_reset_email(user):
    """Send an email to a user with a token to reset their password.
    
    Args:
        user: The user requesting the password reset
    """
    token = user.get_reset_password_token()
    send_email(
        '[PERVADE Coding] Reset Your Password',
        sender=current_app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template(
            'email/reset_password.txt',
            user=user,
            token=token
        ),
        html_body=render_template(
            'email/reset_password.html',
            user=user,
            token=token
        )
    )