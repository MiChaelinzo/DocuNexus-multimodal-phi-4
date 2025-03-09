"""
Handles parsing of various document formats (PDF, DOCX, TXT, etc.)
to extract text content for DocuNexus AGI-Agent. Now Azure-enabled.
"""

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from pypdf import PdfReader  # For PDF parsing fallback
from docx import Document  # For DOCX parsing fallback
import io  # For BytesIO
from src.utils.logger import logger  # Import logger

class AzureDocumentParser:
    def __init__(self, azure_endpoint, azure_api_key):
        """
        Initializes the AzureDocumentParser with Azure Cognitive Services.

        Args:
            azure_endpoint (str): Azure endpoint for Form Recognizer or related services.
            azure_api_key (str): API key for the Azure Form Recognizer.
        """
        self.document_analysis_client = DocumentAnalysisClient(
            endpoint=azure_endpoint,
            credential=AzureKeyCredential(azure_api_key)
        )
        logger.info("AzureDocumentParser initialized with Azure Cognitive Services.")

    def parse_document(self, uploaded_file):
        """
        Parses the uploaded file based on its file extension and extracts text content.

        Args:
            uploaded_file (streamlit.UploadedFile): Streamlit uploaded file object.

        Returns:
            str: Extracted text content from the document, or None if parsing fails.
        """
        file_extension = uploaded_file.name.split(".")[-1].lower()
        logger.debug(f"Parsing document: {uploaded_file.name}, extension: {file_extension}")

        try:
            if file_extension in ["pdf", "jpeg", "jpg", "png"]:
                return self._parse_with_azure(uploaded_file)
            elif file_extension == "docx":
                return self._parse_docx(uploaded_file)
            elif file_extension == "txt":
                return self._parse_txt(uploaded_file)
            else:
                logger.warning(f"Unsupported document format: {file_extension}")
                return None  # Indicate unsupported format
        except Exception as e:
            logger.error(f"Error parsing document: {uploaded_file.name} - {e}")
            return None  # Indicate parsing failure

    def _parse_with_azure(self, uploaded_file):
        """Parses PDF and image files using Azure Form Recognizer."""
        text_content = ""
        try:
            poller = self.document_analysis_client.begin_analyze_document(
                model_id="prebuilt-read",
                document=io.BytesIO(uploaded_file.read())
            )
            result = poller.result()

            for page in result.pages:
                for line in page.lines:
                    text_content += line.content + "\n"

            logger.debug(f"Azure Form Recognizer parsed document successfully: {uploaded_file.name}")
            return text_content
        except Exception as e:
            logger.error(f"Error using Azure Form Recognizer: {uploaded_file.name} - {e}")
            return ""  # Return empty string on parsing error

    def _parse_docx(self, uploaded_file):
        """Parses DOCX files using python-docx library."""
        text_content = ""
        try:
            docx_document = Document(uploaded_file)
            for paragraph in docx_document.paragraphs:
                text_content += paragraph.text + "\n"  # Add newline between paragraphs
            logger.debug(f"DOCX parsed successfully: {uploaded_file.name}")
            return text_content
        except Exception as e:
            logger.error(f"Error parsing DOCX: {uploaded_file.name} - {e}")
            return ""  # Return empty string on parsing error

    def _parse_txt(self, uploaded_file):
        """Parses TXT files (simple text extraction)."""
        try:
            text_content = uploaded_file.read().decode()  # Decode bytes to string (assuming UTF-8)
            logger.debug(f"TXT parsed successfully: {uploaded_file.name}")
            return text_content
        except Exception as e:
            logger.error(f"Error parsing TXT: {uploaded_file.name} - {e}")
            return ""  # Return empty string on parsing error


# --- Example Usage (outside class definition) ---
if __name__ == "__main__":
    azure_endpoint = "YOUR_AZURE_ENDPOINT"  # Replace with your Azure endpoint
    azure_api_key = "YOUR_AZURE_API_KEY"  # Replace with your Azure API key
    parser = AzureDocumentParser(azure_endpoint, azure_api_key)

    # To test, you would need to create dummy files (e.g., "sample.pdf", "sample.docx", "sample.txt")
    # Example usage would be within the Streamlit app when handling file uploads:
    # uploaded_file = st.file_uploader("Upload document", type=["pdf", "docx", "txt", "jpeg", "png"])
    # if uploaded_file:
    #     extracted_text = parser.parse_document(uploaded_file)
    #     if extracted_text:
    #         st.write("Extracted Text (first 200 chars):", extracted_text[:200])
    #     else:
    #         st.error("Document parsing failed.")
    print("AzureDocumentParser example usage demonstrated in comments.")
