from datetime import datetime
import unittest
from flask import url_for, json
from flask_login import current_user
from app import create_app, db
from config import TestConfig
from app.models import User, Code, Award


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username, password):
        return self.client.post(url_for('auth.login'), data={
            'username': username,
            'password': password
        }, follow_redirects=True)

    def logout(self):
        return self.client.get(url_for('auth.logout'), follow_redirects=True)

    def register_user(self, username, email, password1, password2):
        return self.client.post(url_for('auth.register'), data={
            'username': username,
            'email': email,
            'password': password1,
            'password2': password2
        }, follow_redirects=True)

    @staticmethod
    def create_user(username, email, password):
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def create_award(award_id):
        award = Award(award_id=award_id, pi_name='test',
                     contact='test', pi_email='test',
                     organization='test', program='test',
                     title='test', abstract='test')
        db.session.add(award)
        db.session.commit()
        return award
    
    @staticmethod
    def create_code(award, user):
        code = Code(time=datetime.utcnow(), pervasive_data=False,
                    data_science=False, big_data=False,
                    data_synonyms='None', comments='None')
        award.codes.append(code)
        user.codes.append(code)
        db.session.add(award)
        db.session.commit()
        return code


    def test_password_hashing(self):
        user = self.create_user('Eddie', 'test1@test.com', 'my password')
        self.assertTrue(user.username == 'Eddie')
        self.assertFalse(user.check_password('not my password'))
        self.assertTrue(user.check_password('my password'))

    def test_register_and_login(self):
        # Register new account
        response = self.register_user('Eddie', 'test1@test.com', 'test1', 'test1')
        self.assertTrue(response.status_code == 200)

        response = self.login('Eddie', 'test1')
        self.assertTrue(current_user.username == 'Eddie')
        response = self.logout()
        self.assertFalse(current_user.username == 'Eddie')

    def test_available_for_coding(self):
        user1 = self.create_user('Eddie', 'test1@test.com', 'test')
        user2 = self.create_user('Freddy', 'test2@test.com', 'test')
        award1 = self.create_award(1)
        code1 = self.create_code(award1, user1)
        self.login('Eddie', 'test')
        self.assertFalse(award1.available_for_coding(user1))
        self.assertTrue(award1.available_for_coding(user2))

    def test_coding(self):
        user = self.create_user('Eddie', 'test1@test.com', 'test')
        award = self.create_award(award_id=1)
        response = self.login('Eddie', 'test')

        # Get an award
        response = self.client.get(url_for('coding.get_award'), follow_redirects=True)
        print(response.__dict__)
        json_response = json.loads(response.get_data())
        #json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['award'].id == 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)