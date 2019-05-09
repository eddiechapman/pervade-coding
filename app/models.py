from datetime import datetime
from time import time
import jwt
from app import db, login
from flask import session, current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """Represents a user account.

    Attributes:
        id (str): A column of ID numbers.
        username: A column of user names.
        email: A column of user emails.
        password_hash: A column of hashed user passwords.
        codes: A relationship linking the user to the codes they submit.

    """
    __tablename__ = 'user'
    id  = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    codes = db.relationship('Code', back_populates='user')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """
        Store a hashed version of the password in the user table.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Return true if password matches hash, false otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        """
        Create a unique token for resetting a password
        """
        return jwt.encode(
            {'reset_password': self.id,
             'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256',
        ).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token,
                            current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            print('error')
            return

        return User.query.get(id)


@login.user_loader
def load_user(id):
    """Return the user object using a user ID.
    
    Required by flask-login.

    Args:
        id (int): The ID of the current user

    Returns:
        (object): The user's account object.
    """
    return User.query.get(int(id))


class Award(db.Model):
    """
    Represents a research grant from the National Science Foundation.
    """
    __tablename__ = 'award'
    id = db.Column(db.Integer, primary_key=True)
    award_id = db.Column(db.Integer, unique=True)
    pi_name = db.Column(db.String(300))
    contact = db.Column(db.String(1000))
    pi_email = db.Column(db.String(128))
    organization = db.Column(db.String(1000))
    program = db.Column(db.String(1000))
    title = db.Column(db.String(1000))
    abstract = db.Column(db.Text)
    codes = db.relationship('Code', back_populates='award')


    def __repr__(self):
        return 'Award id:{0}'.format(self.id)

    def available_for_coding(self, user):
        """Indicate if an award can be coded by a given user.

        Awards must be coded twice by separate users. It also makes
        sure that the award has not been skipped.

        Args:
            user (Object): Account representing the user.

        Returns:
            (boolean): True if award is available, false if not.
        """
        if len(self.codes) > 1:
            return False

        elif user.id in [code.user_id for code in self.codes]:
            return False

        return True


class Code(db.Model):
    """
    Represents the coding of a single NSF award. Applies to either the
    title or abstract.
    """
    __tablename__  = 'code'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    award_id = db.Column(db.Integer, db.ForeignKey('award.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pervasive_data = db.Column(db.Boolean)
    data_science = db.Column(db.Boolean)
    big_data = db.Column(db.Boolean)
    data_synonyms = db.Column(db.Text)
    comments = db.Column(db.Text)
    award = db.relationship('Award', back_populates='codes')
    user = db.relationship('User', back_populates='codes')

    def __repr__(self):
        return f'Coding id: {self.id}, ' \
            f'award: {self.award}, ' \
            f'user: {self.user}, ' \
            f'time: {self.time}'

