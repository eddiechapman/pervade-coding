from time import time
import jwt
from app import app, db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    codes = db.relationship('Code', back_populates='users')

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id,
             'exp': time() + expires_in},
            app.config['SECRET_KEY'],
            algorithm='HS256'
                ).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            print('error')
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


project_awards = db.Table(
        'project_awards',
        db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
        db.Column('award_id', db.Integer, db.ForeignKey('award.id'))
)


class Award(db.Model):
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
    codes = db.relationship('Code', back_populates='code.award')
    projects = db.relationship('Project', secondary=project_awards, back_populates='awards')

    def __repr__(self):
        return 'Award id:{0}'.format(self.id)


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    codes = db.relationship('Code', back_populates='code.project')
    awards = db.relationship('Award', secondary=project_awards, back_populates='projects')


class Code(db.Model):
    __tablename__ = 'code'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    award_id = db.Column(db.Integer, db.ForeignKey('award.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    code_type = db.Column(db.String(45))
    award = db.relationship('Award', back_populates='codes')
    project = db.relationship('Project', back_populates='codes')
    user = db.relationship('User', back_populates='codes')

    __mapper_args__ = {
            'polymorphic_identity': 'code',
            'polymorphic_on': code_type
    }

    # TODO: Make this more useful considering inheritance.
    def __repr__(self):
        return 'Coding id: {0}, award: {1}, user: {2}, time: {3}'.format(
                self.id,
                self.award,
                self.category,
                self.user,
                self.time
        )


class Title(Code):
    __tablename__ = 'title'
    id = db.Column(db.Integer, db.ForeignKey('code.id'), primary_key=True)
    pervasive_data = db.Column(db.Boolean)
    data_sci = db.Column(db.Boolean)
    big_data = db.Column(db.Boolean)
    case_study = db.Column(db.Boolean)
    data_synonyms = db.Column(db.Text)

    __mapper_args__ = {
            'polymorphic_identity': 'title'
    }

class Abstract(Code):
    __tablename__ = 'abstract'
    id = db.Column(db.Integer, db.ForeignKey('code.id'), primary_key=True)
    pervasive_data = db.Column(db.Boolean)
    data_sci = db.Column(db.Boolean)
    big_data = db.Column(db.Boolean)
    case_study = db.Column(db.Boolean)
    data_synonyms = db.Column(db.Text)

    __mapper_args__ = {
            'polymorphic_identity': 'abstract'
    }
