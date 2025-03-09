import unittest
from src.document_analysis.metadata_handler import MetadataHandler

class TestMetadataHandler(unittest.TestCase):

    def setUp(self):
        self.handler = MetadataHandler()

    def test_extract_metadata_pdf(self):
        metadata = self.handler.extract_metadata("sample.pdf")
        self.assertIsInstance(metadata, dict)
        self.assertIn("Title", metadata)

    def test_extract_metadata_docx(self):
        metadata = self.handler.extract_metadata("sample.docx")
        self.assertIsInstance(metadata, dict)
        self.assertIn("Author", metadata)

if __name__ == '__main__':
    unittest.main()
