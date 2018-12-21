from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail


# TODO: What does this do?
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    """Send an email from the app to a user.
    
    Args:
        subject (str): Text for the email's subject line.
        sender (str): The email account in the email's sender line.
        recipients (str): The email accounts that will receive the email.
        text_body (str): What will the email say in the body?
        html_body (str): The HTML template for formatting the email body.
    """
    msg = Message(
        subject,
        sender=sender,
        recipients=recipients
    )
    msg.body = text_body
    msg.html = html_body
    Thread(
        target=send_async_email,
        args=(current_app._get_current_object(), msg)
    ).start()
