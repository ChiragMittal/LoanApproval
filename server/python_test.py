import unittest
from unittest.mock import MagicMock, patch
import requests

from main import RiskAssessment, all_users


def get_data_from_api(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def post_data_to_api(url, data):
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return None


class TestLoanApprovalSystem(unittest.TestCase):

    def setUp(self):
        # Create a mock for the external dependencies
        self.external_dependency_mock = MagicMock()

    def test_risk_assessment(self):
        # Create a sample loan application for testing
        loan_application = {
            "application_name": "John Doe",
            "credit_score": 700,
            "loan_amount": 5000,
            "loan_purpose": "Home improvement",
            "income": 60000,
            "employment_status": "Employed"
        }

        # Create an instance of RiskAssessment with the mocked external dependency
        risk_assessment = RiskAssessment()

        # Call the method being tested
        risk_score = risk_assessment.assess_risk(loan_application)

        # Assert the expected behavior
        self.assertEqual(risk_score, 0.48958333333333337)

    @patch('requests.get')  # Patch the requests.get method
    def test_get_all_users(self, mock_get):
        # Set up the mock response for a successful API call
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "id": "5bc2425c-ef30-43e8-b7a1-b81d497b1140",
            "name": "Test User"
        }]
        mock_get.return_value = mock_response

        # Call the function under test
        result = get_data_from_api('http://127.0.0.1:5000/all_users')

        # Assertions
        self.assertEqual(result, [{
            "id": "5bc2425c-ef30-43e8-b7a1-b81d497b1140",
            "name": "Test User"
        }])
        mock_get.assert_called_once_with('http://127.0.0.1:5000/all_users')

    @patch('requests.get')  # Patch the requests.get method
    def test_get_all_applications(self, mock_get):
        # Set up the mock response for a successful API call
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "application_name": "CM 1",
            "credit_score": 750,
            "employment_status": "Employed",
            "id": "609b48cd-adef-4417-bfab-452d5a7bca68",
            "income": 10000.0,
            "loan_amount": 100.0,
            "loan_purpose": "TP",
            "user_id": "5bc2425c-ef30-43e8-b7a1-b81d497b1140"
        }]
        mock_get.return_value = mock_response

        # Call the function under test
        result = get_data_from_api('http://127.0.0.1:5000/get_all_loan_applications')

        # Assertions
        self.assertEqual(result, [{
            "application_name": "CM 1",
            "credit_score": 750,
            "employment_status": "Employed",
            "id": "609b48cd-adef-4417-bfab-452d5a7bca68",
            "income": 10000.0,
            "loan_amount": 100.0,
            "loan_purpose": "TP",
            "user_id": "5bc2425c-ef30-43e8-b7a1-b81d497b1140"
        }])
        mock_get.assert_called_once_with('http://127.0.0.1:5000/get_all_loan_applications')

    @patch('requests.post')  # Patch the requests.post method
    def test_post_new_user(self, mock_post):
        # Set up the mock response for a successful API POST
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Test User 1"
        }
        mock_post.return_value = mock_response

        # Call the function under test
        data_to_post = {
            "name": "Test User 1"
        }
        result = post_data_to_api('http://127.0.0.1:5000/create_new_user', data_to_post)
        # Assertions
        self.assertEqual(result, {
            "name": "Test User 1"
        })
        mock_post.assert_called_once_with('http://127.0.0.1:5000/create_new_user', json=data_to_post)

    @patch('requests.post')  # Patch the requests.post method
    def test_post_new_application(self, mock_post):
        # Set up the mock response for a successful API POST
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "application_name": "CM 1",
            "credit_score": 750,
            "employment_status": "Employed",
            "income": 10000.0,
            "loan_amount": 100.0,
            "loan_purpose": "TP",
            "user_id": "5bc2425c-ef30-43e8-b7a1-b81d497b1140"
        }
        mock_post.return_value = mock_response

        # Call the function under test
        data_to_post = {
            "application_name": "CM 1",
            "credit_score": 750,
            "employment_status": "Employed",
            "income": 10000.0,
            "loan_amount": 100.0,
            "loan_purpose": "TP",
            "user_id": "5bc2425c-ef30-43e8-b7a1-b81d497b1140"
        }
        result = post_data_to_api('http://127.0.0.1:5000/create_new_loan_application', data_to_post)
        # Assertions
        self.assertEqual(result, {
            "application_name": "CM 1",
            "credit_score": 750,
            "employment_status": "Employed",
            "income": 10000.0,
            "loan_amount": 100.0,
            "loan_purpose": "TP",
            "user_id": "5bc2425c-ef30-43e8-b7a1-b81d497b1140"
        })
        mock_post.assert_called_once_with('http://127.0.0.1:5000/create_new_loan_application', json=data_to_post)

    @patch('requests.post')  # Patch the requests.post method
    def test_post_get_status(self, mock_post):
        # Set up the mock response for a successful API POST
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "loan_application_id": "609b48cd-adef-4417-bfab-452d5a7bca68",
            "risk_score": 0.486875,
            "status": "Approved"
        }
        mock_post.return_value = mock_response

        # Call the function under test
        data_to_post = {
            "id": "a2a97421-fd2e-48ce-937d-14b2517b068d",
        }
        result = post_data_to_api('http://127.0.0.1:5000/get_status', data_to_post)
        # Assertions
        self.assertEqual(result, {
            "loan_application_id": "609b48cd-adef-4417-bfab-452d5a7bca68",
            "risk_score": 0.486875,
            "status": "Approved"
        })
        mock_post.assert_called_once_with('http://127.0.0.1:5000/get_status', json=data_to_post)

    @patch('requests.post')  # Patch the requests.post method
    def test_post_delete_all_user(self, mock_post):
        # Set up the mock response for a successful API POST
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'message': 'User deleted successfully'}
        mock_post.return_value = mock_response

        # Call the function under test
        data_to_post = {

        }
        result = post_data_to_api('http://127.0.0.1:5000/delete_all_user', data_to_post)
        # Assertions
        self.assertEqual(result, {'message': 'User deleted successfully'})
        mock_post.assert_called_once_with('http://127.0.0.1:5000/delete_all_user', json=data_to_post)

    @patch('requests.post')  # Patch the requests.post method
    def test_post_delete_all_applications(self, mock_post):
        # Set up the mock response for a successful API POST
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'message': 'Application deleted successfully'}
        mock_post.return_value = mock_response

        # Call the function under test
        data_to_post = {

        }
        result = post_data_to_api('http://127.0.0.1:5000/delete_all_application', data_to_post)
        # Assertions
        self.assertEqual(result, {'message': 'Application deleted successfully'})
        mock_post.assert_called_once_with('http://127.0.0.1:5000/delete_all_application', json=data_to_post)


if __name__ == '__main__':
    unittest.main()
