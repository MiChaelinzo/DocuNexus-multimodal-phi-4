import unittest
from src.document_analysis.document_parser import DocumentParser

class TestDocumentParser(unittest.TestCase):

    def setUp(self):
        self.parser = DocumentParser()

    def test_parse_pdf(self):
        text = self.parser.parse_pdf("sample.pdf")
        self.assertIsInstance(text, str)
        self.assertIn("Sample", text)

    def test_parse_docx(self):
        text = self.parser.parse_docx("sample.docx")
        self.assertIsInstance(text, str)
        self.assertIn("Sample", text)

if __name__ == '__main__':
    unittest.main()
