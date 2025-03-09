"""
Azure-enabled module for DocuSign API integration for DocuNexus AGI-Agent.
Handles sending documents for signature via the DocuSign API, with Azure Blob Storage for document management.
"""

from azure.storage.blob import BlobServiceClient
import requests
import base64
import tempfile
from src.utils.config import AppConfig  # For API key retrieval from config
from src.utils.logger import logger  # Import logger


class AzureDocuSignIntegration:
    def __init__(self, docusign_api_key, docusign_base_url, docusign_account_id, storage_connection_string):
        """
        Initializes AzureDocuSignIntegration with DocuSign API and Azure Blob Storage.

        Args:
            docusign_api_key (str): DocuSign API key.
            docusign_base_url (str): Base URL for DocuSign API (e.g., https://demo.docusign.net/restapi).
            docusign_account_id (str): Account ID for DocuSign API.
            storage_connection_string (str): Azure Blob Storage connection string.
        """
        self.docusign_api_key = docusign_api_key
        self.docusign_base_url = docusign_base_url
        self.docusign_account_id = docusign_account_id
        self.blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
        logger.info("Azure-enabled DocuSign Integration initialized.")

    def upload_document_to_blob(self, local_file_path, container_name):
        """
        Uploads a document to Azure Blob Storage.

        Args:
            local_file_path (str): Path to the local document file.
            container_name (str): Name of the Blob Storage container.

        Returns:
            str: URL of the uploaded Blob.
        """
        logger.info(f"Uploading document to Azure Blob Storage: {local_file_path}")
        try:
            blob_name = local_file_path.split("/")[-1]
            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)

            with open(local_file_path, "rb") as file:
                blob_client.upload_blob(file, overwrite=True)
            logger.info(f"Document uploaded successfully to Blob Storage: {blob_client.url}")
            return blob_client.url
        except Exception as e:
            logger.error(f"Error uploading document to Azure Blob Storage: {e}")
            raise

    def send_to_docusign(self, local_file_path, recipient_email, recipient_name):
        """
        Sends a document for signature via the DocuSign API.

        Args:
            local_file_path (str): Path to the local document file.
            recipient_email (str): Recipient's email address.
            recipient_name (str): Recipient's name.

        Returns:
            dict: Response from the DocuSign API.
        """
        logger.info(f"Sending document to DocuSign for: {recipient_email}")

        try:
            # Read the file and encode it to base64
            with open(local_file_path, "rb") as file:
                document_base64 = base64.b64encode(file.read()).decode("utf-8")

            # Prepare envelope definition
            envelope_definition = {
                "emailSubject": "Please sign this document",
                "documents": [
                    {
                        "documentId": "1",
                        "name": local_file_path.split("/")[-1],
                        "fileExtension": "pdf",
                        "documentBase64": document_base64,
                    }
                ],
                "recipients": {
                    "signers": [
                        {
                            "email": recipient_email,
                            "name": recipient_name,
                            "recipientId": "1",
                            "tabs": {
                                "signHereTabs": [
                                    {
                                        "documentId": "1",
                                        "pageNumber": "1",
                                        "xPosition": "150",
                                        "yPosition": "200",
                                    }
                                ]
                            },
                        }
                    ]
                },
                "status": "sent",
            }

            # Make API request to DocuSign
            headers = {
                "Authorization": f"Bearer {self.docusign_api_key}",
                "Content-Type": "application/json",
            }
            response = requests.post(
                f"{self.docusign_base_url}/v2.1/accounts/{self.docusign_account_id}/envelopes",
                headers=headers,
                json=envelope_definition,
            )

            if response.status_code == 201:
                logger.info("Document sent to DocuSign successfully.")
                return response.json()
            else:
                logger.error(f"Error sending to DocuSign: {response.status_code} - {response.text}")
                return {"status": "error", "message": response.text}

        except Exception as e:
            logger.error(f"Error during DocuSign API call: {e}")
            return {"status": "error", "message": str(e)}


# --- Example Usage ---
if __name__ == "__main__":
    DOCUSIGN_API_KEY = "YOUR_DOCUSIGN_API_KEY"
    DOCUSIGN_BASE_URL = "https://demo.docusign.net/restapi"
    DOCUSIGN_ACCOUNT_ID = "YOUR_ACCOUNT_ID"
    STORAGE_CONNECTION_STRING = "YOUR_AZURE_STORAGE_CONNECTION_STRING"
    CONTAINER_NAME = "documents"

    docusign_integration = AzureDocuSignIntegration(
        docusign_api_key=DOCUSIGN_API_KEY,
        docusign_base_url=DOCUSIGN_BASE_URL,
        docusign_account_id=DOCUSIGN_ACCOUNT_ID,
        storage_connection_string=STORAGE_CONNECTION_STRING,
    )

    # Local document path
    local_file_path = "sample_document.pdf"
    recipient_email = "test.recipient@example.com"
    recipient_name = "Test Recipient"

    # Upload the document to Azure Blob Storage
    blob_url = docusign_integration.upload_document_to_blob(local_file_path, CONTAINER_NAME)
    print(f"Document uploaded to Azure Blob Storage: {blob_url}")

    # Send the document to DocuSign for signature
    docusign_response = docusign_integration.send_to_docusign(local_file_path, recipient_email, recipient_name)
    print("\n--- DocuSign Integration Response ---")
    print(docusign_response)
