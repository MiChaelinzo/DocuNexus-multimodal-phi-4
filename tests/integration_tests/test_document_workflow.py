import unittest
from src.document_analysis.document_parser import DocumentParser
from src.document_analysis.metadata_handler import MetadataHandler
from src.core.agi_engine import AGIEngine

class TestDocumentWorkflow(unittest.TestCase):

    def setUp(self):
        self.parser = DocumentParser()
        self.metadata_handler = MetadataHandler()
        self.agi_engine = AGIEngine()

    def test_document_workflow(self):
        # Step 1: Parse document
        document_text = self.parser.parse_pdf("sample_document.pdf")
        self.assertIsInstance(document_text, str)
        self.assertTrue(len(document_text) > 0)

        # Step 2: Extract metadata
        metadata = self.metadata_handler.extract_metadata("sample_document.pdf")
        self.assertIsInstance(metadata, dict)
        self.assertIn("Title", metadata)

        # Step 3: Summarize document
        response, thoughts = self.agi_engine.process_text_request(
            "Summarize this document.",
            context_documents=[document_text]
        )
        self.assertIsInstance(response, str)
        self.assertIn("summary", response.lower())

if __name__ == '__main__':
    unittest.main()
