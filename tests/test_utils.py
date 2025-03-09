"""
Utility functions and data for unit and integration tests in DocuNexus AGI-Agent.
Includes mock objects, test data loading, and helper functions for test setup/assertions.
"""

from azure.storage.blob import BlobServiceClient
import json
import os
import tempfile

# --- Example Placeholder Mock Objects (for unit testing Azure services) ---
class MockAzureAIModel:
    """Mock object to simulate Azure OpenAI model behavior."""
    def __init__(self, mock_response_text="Mock AI Response"):
        self.mock_response_text = mock_response_text

    def get_chat_completions(self, model, messages, max_tokens=500):
        """Simulate Azure OpenAI's chat completion API."""
        return {"choices": [{"message": {"content": self.mock_response_text}}]}


class MockBlobServiceClient:
    """Mock object to simulate Azure Blob Storage behavior."""
    def __init__(self):
        self.storage = {}

    def get_blob_client(self, container, blob):
        """Returns a mock blob client."""
        return MockBlobClient(self.storage, container, blob)


class MockBlobClient:
    """Mock client for interacting with Azure Blob Storage."""
    def __init__(self, storage, container, blob):
        self.storage = storage
        self.container = container
        self.blob = blob

    def upload_blob(self, data, overwrite=False):
        """Simulate blob upload."""
        if self.container not in self.storage:
            self.storage[self.container] = {}
        self.storage[self.container][self.blob] = data
        return True

    def download_blob(self):
        """Simulate blob download."""
        return self.storage[self.container][self.blob]

    def exists(self):
        """Check if the blob exists."""
        return self.container in self.storage and self.blob in self.storage[self.container]


# --- Example Test Data (Placeholder) ---
SAMPLE_DOCUMENT_TEXT = """
This is a sample document for testing.
It contains some text that can be summarized or analyzed by DocuNexus AGI.
"""

SAMPLE_PROMPT = "Summarize this document."

SAMPLE_BLOB_NAME = "test_document.pdf"
SAMPLE_CONTAINER_NAME = "test-container"

# --- Example Helper Functions ---
def upload_mock_blob(data, container_name, blob_name):
    """
    Simulates uploading a blob to Azure Blob Storage.
    """
    mock_blob_service = MockBlobServiceClient()
    blob_client = mock_blob_service.get_blob_client(container_name, blob_name)
    blob_client.upload_blob(data, overwrite=True)
    print(f"Uploaded mock blob: {blob_name} to container: {container_name}")
    return mock_blob_service


def assert_blob_exists(mock_blob_service, container_name, blob_name):
    """
    Assert that a blob exists in the mocked Azure Blob Storage.
    """
    assert mock_blob_service.get_blob_client(container_name, blob_name).exists(), f"Blob {blob_name} does not exist in container {container_name}."
    print(f"Assertion passed: Blob {blob_name} exists in container {container_name}.")


def assert_response_contains(response_text, expected_substrings):
    """
    Assert that the response text contains all expected substrings.
    """
    if not isinstance(expected_substrings, list):
        expected_substrings = [expected_substrings]

    for substr in expected_substrings:
        assert substr in response_text, f"Response text does not contain expected substring: '{substr}'"
    print("Assertion passed: Response contains all expected substrings.")


def generate_temp_file(content, suffix=".txt"):
    """
    Generate a temporary file with the specified content.
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_file.write(content.encode('utf-8'))
    temp_file.close()
    return temp_file.name


# --- Example Usage ---
if __name__ == "__main__":
    # Example: Using MockAzureAIModel
    mock_model = MockAzureAIModel(mock_response_text="This is a mocked response from Azure OpenAI.")
    result = mock_model.get_chat_completions(
        model="gpt-4",
        messages=[{"role": "user", "content": SAMPLE_PROMPT}],
    )
    assert_response_contains(result["choices"][0]["message"]["content"], "mocked response")

    # Example: Mocking Azure Blob Storage
    mock_blob_service = upload_mock_blob(SAMPLE_DOCUMENT_TEXT, SAMPLE_CONTAINER_NAME, SAMPLE_BLOB_NAME)
    assert_blob_exists(mock_blob_service, SAMPLE_CONTAINER_NAME, SAMPLE_BLOB_NAME)

    # Example: Generating a temporary file
    temp_file_path = generate_temp_file(SAMPLE_DOCUMENT_TEXT)
    print(f"Temporary file created at: {temp_file_path}")
