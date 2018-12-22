from datetime import datetime, timedelta
import unittest
from app import create_app, db
from config import TestConfig
from app.models import User, Code, Award
from config import Config


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        user = User(username='Eddie', email='test@test.com')
        user.set_password('my password')
        self.assertTrue(user.username == 'Eddie')
        self.assertFalse(user.check_password('not my password'))
        self.assertTrue(user.check_password('my password'))


    def test_coding(self):
        award1 = Award(
            award_id=1,
            pi_name='test',
            contact='test',
            pi_email='test',
            organization='test',
            program='test',
            title='test',
            abstract='test',
        )
        award2 = Award(
            award_id=2,
            pi_name='test',
            contact='test',
            pi_email='test',
            organization='test',
            program='test',
            title='test',
            abstract='test'
        )
        user1 = User(username='Eddie', email='test@test.com')
        user2 = User(username='Freddy', email='test@test.com')
        #TODO: Update coding.html to show both subforms
        #TODO: Figure out how to test the forms

    def test_skip_award(self):
        pass

    def test_double_code(self):
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)