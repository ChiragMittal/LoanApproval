import unittest
import json
from main import app, session, db_connect, User, LoanApplication, LoanStatus, RiskAssessment

class FlaskAppTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.session = session
        self.db_connect = db_connect

    def tearDown(self):
        # Rollback the database session after each test
        self.session.rollback()

    def test_get_all_loan_applications(self):
        response = self.app.get('/get_all_loan_applications')
        self.assertEqual(response.status_code, 200)

    def test_all_users(self):
        response = self.app.get('/all_users')
        self.assertEqual(response.status_code, 200)

    def test_create_new_user(self):
        data = {"name": "John Doe"}
        response = self.app.post('/create_new_user', json={'data': data})
        self.assertEqual(response.status_code, 201)

    def test_create_new_loan_application(self):
        user_data = {"name": "Test User"}
        user_response = self.app.post('/create_new_user', json={'data': user_data})
        self.assertEqual(user_response.status_code, 201)

    def test_get_status(self):
        loan_data = {
            "application_name": "Test Application",
            "user_id": "1",  # Replace with an existing user_id from your database
            "credit_score": 700,
            "loan_purpose": "Home",
            "loan_amount": 10000.0,
            "income": 50000.0,
            "employment_status": "Employed"
        }
        loan_response = self.app.post('/create_new_loan_application', json={'data': loan_data})

        # Inspect the response data structure
        response_data = json.loads(loan_response.data)
        self.assertEqual(loan_response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
