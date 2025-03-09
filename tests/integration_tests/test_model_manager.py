import unittest
from src.core.model_manager import ModelManager

class TestModelManager(unittest.TestCase):

    def setUp(self):
        self.manager = ModelManager()

    def test_get_model_default(self):
        model = self.manager.get_model()
        self.assertIsNotNone(model)
        self.assertEqual(model.model_name, "gpt-4")  # Assuming default is GPT-4

    def test_get_model_phi4(self):
        model = self.manager.get_model(use_phi4=True)
        self.assertIsNotNone(model)
        self.assertEqual(model.model_name, "phi-4-multimodal-instruct")  # Assuming this for Phi-4

if __name__ == '__main__':
    unittest.main()
