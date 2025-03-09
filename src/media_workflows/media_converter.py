"""
Azure-enabled module for media format conversion within DocuNexus AGI-Agent.
Utilizes Azure Media Services for scalable and efficient media transcoding and processing.
"""

import os
import time
from azure.identity import DefaultAzureCredential
from azure.mgmt.media import AzureMediaServices
from azure.mgmt.media.models import (
    Asset,
    Job,
    Transform,
    TransformOutput,
    StandardEncoderPreset,
    OnErrorType,
    Priority
)
from azure.storage.blob import BlobServiceClient
from src.utils.logger import logger  # Import logger

class AzureMediaConverter:
    def __init__(self, subscription_id, resource_group_name, account_name, storage_connection_string):
        """
        Initializes AzureMediaConverter with Azure Media Services.

        Args:
            subscription_id (str): Azure subscription ID.
            resource_group_name (str): Resource group name for Azure Media Services.
            account_name (str): Azure Media Services account name.
            storage_connection_string (str): Azure Blob Storage connection string for asset storage.
        """
        self.subscription_id = subscription_id
        self.resource_group_name = resource_group_name
        self.account_name = account_name
        self.storage_client = BlobServiceClient.from_connection_string(storage_connection_string)
        self.media_client = AzureMediaServices(DefaultAzureCredential(), subscription_id)
        logger.info("AzureMediaConverter initialized with Azure Media Services and Blob Storage.")

    def create_asset(self, asset_name):
        """
        Creates an asset in Azure Media Services for storing media files.

        Args:
            asset_name (str): Name of the asset to be created.

        Returns:
            Asset: The created Asset object.
        """
        logger.info(f"Creating asset: {asset_name}")
        try:
            asset = self.media_client.assets.create_or_update(
                resource_group_name=self.resource_group_name,
                account_name=self.account_name,
                asset_name=asset_name,
                parameters=Asset()
            )
            logger.info(f"Asset '{asset_name}' created successfully.")
            return asset
        except Exception as e:
            logger.error(f"Error creating asset '{asset_name}': {e}")
            raise

    def upload_to_asset(self, asset_name, file_path):
        """
        Uploads a media file to the Azure Blob Storage container associated with an Asset.

        Args:
            asset_name (str): Name of the Asset.
            file_path (str): Path to the media file.
        """
        logger.info(f"Uploading file to asset '{asset_name}': {file_path}")
        try:
            container_name = f"asset-{asset_name.lower()}"
            blob_name = os.path.basename(file_path)
            blob_client = self.storage_client.get_blob_client(container=container_name, blob=blob_name)

            with open(file_path, "rb") as file:
                blob_client.upload_blob(file, overwrite=True)
            logger.info(f"File '{file_path}' uploaded to asset '{asset_name}' successfully.")
        except Exception as e:
            logger.error(f"Error uploading file to asset '{asset_name}': {e}")
            raise

    def create_transform(self, transform_name, output_format):
        """
        Creates a Transform in Azure Media Services for transcoding.

        Args:
            transform_name (str): Name of the Transform.
            output_format (str): Desired output format (e.g., "MP4", "MOV").

        Returns:
            Transform: The created Transform object.
        """
        logger.info(f"Creating transform: {transform_name} for output format: {output_format}")
        try:
            transform_output = TransformOutput(
                preset=StandardEncoderPreset(
                    codecs=[],
                    formats=[{"type": output_format}]
                ),
                on_error=OnErrorType.STOP_PROCESSING_JOB,
                relative_priority=Priority.NORMAL
            )

            transform = self.media_client.transforms.create_or_update(
                resource_group_name=self.resource_group_name,
                account_name=self.account_name,
                transform_name=transform_name,
                parameters=Transform(outputs=[transform_output])
            )
            logger.info(f"Transform '{transform_name}' created successfully.")
            return transform
        except Exception as e:
            logger.error(f"Error creating transform '{transform_name}': {e}")
            raise

    def submit_job(self, transform_name, input_asset_name, output_asset_name, job_name):
        """
        Submits a transcoding Job to Azure Media Services.

        Args:
            transform_name (str): Name of the Transform to use.
            input_asset_name (str): Name of the input Asset.
            output_asset_name (str): Name of the output Asset.
            job_name (str): Name of the Job.

        Returns:
            Job: The submitted Job object.
        """
        logger.info(f"Submitting job: {job_name}")
        try:
            input = {
                "oDataType": "#Microsoft.Media.JobInputAsset",
                "assetName": input_asset_name
            }
            output = {"assetName": output_asset_name}

            job = self.media_client.jobs.create(
                resource_group_name=self.resource_group_name,
                account_name=self.account_name,
                transform_name=transform_name,
                job_name=job_name,
                parameters=Job(input=input, outputs=[output])
            )
            logger.info(f"Job '{job_name}' submitted successfully.")
            return job
        except Exception as e:
            logger.error(f"Error submitting job '{job_name}': {e}")
            raise

    def wait_for_job_completion(self, transform_name, job_name):
        """
        Waits for a Job to complete and logs its progress.

        Args:
            transform_name (str): Name of the Transform.
            job_name (str): Name of the Job.
        """
        logger.info(f"Waiting for job completion: {job_name}")
        while True:
            job = self.media_client.jobs.get(
                resource_group_name=self.resource_group_name,
                account_name=self.account_name,
                transform_name=transform_name,
                job_name=job_name
            )
            if job.state in ["Finished", "Error", "Canceled"]:
                logger.info(f"Job '{job_name}' completed with state: {job.state}")
                break
            time.sleep(10)


# --- Example Usage ---
if __name__ == "__main__":
    # Replace with your Azure credentials and paths
    SUBSCRIPTION_ID = "YOUR_AZURE_SUBSCRIPTION_ID"
    RESOURCE_GROUP_NAME = "YOUR_RESOURCE_GROUP_NAME"
    ACCOUNT_NAME = "YOUR_MEDIA_SERVICES_ACCOUNT_NAME"
    STORAGE_CONNECTION_STRING = "YOUR_STORAGE_CONNECTION_STRING"

    converter = AzureMediaConverter(
        subscription_id=SUBSCRIPTION_ID,
        resource_group_name=RESOURCE_GROUP_NAME,
        account_name=ACCOUNT_NAME,
        storage_connection_string=STORAGE_CONNECTION_STRING
    )

    input_file_path = "sample.mp4"
    input_asset_name = "input-asset"
    output_asset_name = "output-asset"
    transform_name = "mp4-to-mov-transform"
    job_name = "transcoding-job"

    # Step 1: Create Assets
    converter.create_asset(input_asset_name)
    converter.create_asset(output_asset_name)

    # Step 2: Upload File to Input Asset
    converter.upload_to_asset(input_asset_name, input_file_path)

    # Step 3: Create Transform
    converter.create_transform(transform_name, output_format="MOV")

    # Step 4: Submit Job
    converter.submit_job(transform_name, input_asset_name, output_asset_name, job_name)

    # Step 5: Wait for Job Completion
    converter.wait_for_job_completion(transform_name, job_name)
