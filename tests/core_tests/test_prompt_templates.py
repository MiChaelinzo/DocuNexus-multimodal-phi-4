import unittest
from src.core.prompt_templates import PromptTemplates

class TestPromptTemplates(unittest.TestCase):

    def setUp(self):
        self.templates = PromptTemplates()

    def test_generate_summary_prompt(self):
        prompt = self.templates.generate_summary_prompt("Document text")
        self.assertIn("Summarize", prompt)
        self.assertIn("Document text", prompt)

    def test_generate_comparison_prompt(self):
        prompt = self.templates.generate_comparison_prompt("Doc1 text", "Doc2 text")
        self.assertIn("Compare", prompt)
        self.assertIn("Doc1 text", prompt)
        self.assertIn("Doc2 text", prompt)

if __name__ == '__main__':
    unittest.main()
