import unittest
from azure.storage.blob import BlobServiceClient

class TestAzureBlobStorage(unittest.TestCase):

    def setUp(self):
        connection_string = "YOUR_AZURE_BLOB_CONNECTION_STRING"
        self.client = BlobServiceClient.from_connection_string(connection_string)
        self.container_name = "test-container"

    def test_upload_blob(self):
        blob_client = self.client.get_blob_client(container=self.container_name, blob="test.txt")
        blob_client.upload_blob(b"This is a test blob", overwrite=True)
        self.assertTrue(blob_client.exists())

if __name__ == '__main__':
    unittest.main()
