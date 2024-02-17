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
        user_data = {"name": "Test User"}
        user_response = self.app.post('/create_new_user', json={'data': user_data})
        self.assertEqual(user_response.status_code, 201)

    def test_create_new_loan_application(self):
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

        loan_id = json.loads(loan_response.data).get('id')

        # Retrieve loan status using the loan ID
        status_response = self.app.post('/get_status', json={'id': loan_id})
        assert status_response.status_code == 200

        # Validate the response data or add more assertions as needed
        assert 'risk_score' in json.loads(status_response.data)

        edit_response = self.app.post('/update_application_name', json={'id': loan_id,
         'application_name': "Try"})

        assert edit_response.status_code == 201


if __name__ == '__main__':
    unittest.main()
