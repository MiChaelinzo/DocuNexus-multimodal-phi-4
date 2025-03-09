import unittest
from src.core.response_formatter import ResponseFormatter

class TestResponseFormatter(unittest.TestCase):

    def setUp(self):
        self.formatter = ResponseFormatter()

    def test_format_response_concise(self):
        formatted = self.formatter.format_response("Sample response", "concise")
        self.assertTrue(len(formatted) < 100)  # Assuming concise responses are under 100 characters

    def test_format_response_detailed(self):
        formatted = self.formatter.format_response("Sample response", "detailed")
        self.assertTrue(len(formatted) > 100)  # Assuming detailed responses are longer

if __name__ == '__main__':
    unittest.main()
