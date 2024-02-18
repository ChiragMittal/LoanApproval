import unittest
from unittest.mock import MagicMock

from main import RiskAssessment


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
        self.assertEqual(risk_score, 0.6066666666666666)


if __name__ == '__main__':
    unittest.main()
