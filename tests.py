from datetime import datetime, timedelta
import unittest
from app import create_app, db
from config import TestConfig
from app.models import User, Code
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
        pass

    def test_coding(self):
        pass

    def test_skip_award(self):
        pass

    def test_double_code(self):
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)