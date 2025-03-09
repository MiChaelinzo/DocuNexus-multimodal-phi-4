"""
Azure-enabled module for extracting and managing document metadata within DocuNexus AGI-Agent.
This module integrates with Azure Form Recognizer for metadata extraction and Azure OpenAI for reasoning tasks.
"""

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.openai import OpenAIClient
from azure.core.exceptions import AzureError
from src.utils.logger import logger  # Import logger


class AzureMetadataHandler:
    def __init__(self, form_recognizer_endpoint, form_recognizer_key, openai_endpoint, openai_api_key, model_name="gpt-4"):
        """
        Initializes the AzureMetadataHandler with Azure Cognitive Services.

        Args:
            form_recognizer_endpoint (str): Azure Form Recognizer endpoint.
            form_recognizer_key (str): Azure Form Recognizer API key.
            openai_endpoint (str): Azure OpenAI endpoint.
            openai_api_key (str): Azure OpenAI API key.
            model_name (str): Model name for Azure OpenAI (default: "gpt-4").
        """
        self.form_recognizer_client = DocumentAnalysisClient(
            endpoint=form_recognizer_endpoint,
            credential=AzureKeyCredential(form_recognizer_key)
        )
        self.openai_client = OpenAIClient(
            endpoint=openai_endpoint,
            credential=AzureKeyCredential(openai_api_key)
        )
        self.model_name = model_name
        logger.info("AzureMetadataHandler initialized with Form Recognizer and OpenAI.")

    def extract_metadata(self, document):
        """
        Extracts metadata from the document using Azure Form Recognizer.

        Args:
            document (bytes): The document content in bytes (PDF, image).

        Returns:
            dict: Extracted metadata such as authorship, timestamps, and version history.
        """
        logger.debug("Extracting metadata using Azure Form Recognizer.")

        try:
            poller = self.form_recognizer_client.begin_analyze_document(
                model_id="prebuilt-document",
                document=document
            )
            result = poller.result()

            metadata = {
                "file_name": result.metadata.get("file_name", "Unknown"),
                "file_type": result.metadata.get("file_type", "Unknown"),
                "size": result.metadata.get("file_size", "Unknown"),
                "author": result.metadata.get("author", "Unknown"),
                "creation_date": result.metadata.get("creation_date", "Unknown"),
                "modification_date": result.metadata.get("modification_date", "Unknown")
            }
            logger.info("Metadata extraction completed successfully.")
            return metadata

        except AzureError as e:
            logger.error(f"Error extracting metadata: {e}")
            return {"error": str(e)}

    def analyze_metadata(self, metadata):
        """
        Performs reasoning or insights generation based on the extracted metadata using Azure OpenAI.

        Args:
            metadata (dict): Metadata extracted from the document.

        Returns:
            str: Insights or analysis based on metadata.
        """
        logger.debug("Analyzing metadata using Azure OpenAI.")

        try:
            # Constructing prompt with metadata details
            prompt = "Analyze the following document metadata and provide insights:\n"
            for key, value in metadata.items():
                prompt += f"{key}: {value}\n"

            response = self.openai_client.get_chat_completions(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are an AI expert in document metadata analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500
            )

            insights = response.choices[0].message["content"]
            logger.info("Metadata analysis completed successfully.")
            return insights

        except AzureError as e:
            logger.error(f"Error analyzing metadata: {e}")
            return f"Error occurred: {e}"


# --- Example Usage ---
if __name__ == "__main__":
    # Replace with your Azure credentials
    FORM_RECOGNIZER_ENDPOINT = "YOUR_FORM_RECOGNIZER_ENDPOINT"
    FORM_RECOGNIZER_KEY = "YOUR_FORM_RECOGNIZER_KEY"
    OPENAI_ENDPOINT = "YOUR_OPENAI_ENDPOINT"
    OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

    handler = AzureMetadataHandler(
        form_recognizer_endpoint=FORM_RECOGNIZER_ENDPOINT,
        form_recognizer_key=FORM_RECOGNIZER_KEY,
        openai_endpoint=OPENAI_ENDPOINT,
        openai_api_key=OPENAI_API_KEY
    )

    # Example usage for metadata extraction
    with open("sample.pdf", "rb") as f:
        metadata = handler.extract_metadata(f.read())
        print("\n--- Extracted Metadata ---")
        print(metadata)

    # Example usage for metadata analysis
    if metadata:
        insights = handler.analyze_metadata(metadata)
        print("\n--- Metadata Analysis Insights ---")
        print(insights)
