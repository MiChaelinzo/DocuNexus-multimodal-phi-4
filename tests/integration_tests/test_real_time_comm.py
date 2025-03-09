import unittest
from src.real_time_comm.webcam_integration import WebcamFeedProcessor
from PIL import Image

class TestWebcamIntegration(unittest.TestCase):

    def setUp(self):
        self.processor = WebcamFeedProcessor(None)  # Pass None or a mock AGI engine

    def test_transform_frame(self):
        # Create a dummy image
        img = Image.new("RGB", (100, 100), color="blue")
        transformed_frame = self.processor.transform(img)
        self.assertIsNotNone(transformed_frame)

if __name__ == '__main__':
    unittest.main()
