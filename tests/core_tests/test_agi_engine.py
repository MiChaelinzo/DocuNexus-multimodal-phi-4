import unittest
from src.core.agi_engine import AGIEngine

class TestAGIEngine(unittest.TestCase):

    def setUp(self):
        """Setup runs before each test."""
        self.engine = AGIEngine()

    def test_process_text_request(self):
        """Test the AGIEngine's ability to process text-based requests."""
        prompt = "Summarize the following document: DocuNexus simplifies workflows."
        response, thoughts = self.engine.process_text_request(prompt)
        self.assertIsInstance(response, str)
        self.assertIn("summarize", response.lower())

    def test_process_vision_request(self):
        """Test the AGIEngine's ability to process vision-based requests."""
        prompt = "Describe the objects in this image."
        image_data = b"\x89PNG\r\n\x1a\n..."  # Mock image bytes
        response, thoughts = self.engine.process_vision_request(prompt, image_data)
        self.assertIsInstance(response, str)
        self.assertIn("describe", response.lower())

if __name__ == "__main__":
    unittest.main()
