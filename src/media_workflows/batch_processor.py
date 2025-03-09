"""
Azure-enabled module for batch processing of media files within DocuNexus AGI-Agent.
Leverages Azure Blob Storage for file management and Azure Batch for distributed processing.
"""

import os
import tempfile
from azure.storage.blob import BlobServiceClient
from azure.batch import BatchServiceClient
from azure.batch.models import (
    PoolAddParameter,
    VirtualMachineConfiguration,
    CloudServiceConfiguration,
    TaskAddParameter,
)
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from src.utils.logger import logger  # Import logger


class AzureBatchProcessor:
    def __init__(self, storage_connection_string, batch_account_name, batch_account_url):
        """
        Initializes AzureBatchProcessor with Azure Blob Storage and Batch Services.

        Args:
            storage_connection_string (str): Azure Blob Storage connection string.
            batch_account_name (str): Azure Batch account name.
            batch_account_url (str): Azure Batch account URL.
        """
        self.blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
        self.batch_client = BatchServiceClient(
            credential=DefaultAzureCredential(),
            batch_url=batch_account_url
        )
        self.batch_account_name = batch_account_name
        logger.info("AzureBatchProcessor initialized with Blob Storage and Azure Batch.")

    def upload_files_to_blob(self, container_name, directory_path):
        """
        Uploads all files in a directory to an Azure Blob Storage container.

        Args:
            container_name (str): Name of the container to upload files to.
            directory_path (str): Path to the directory containing files.

        Returns:
            list: List of blob URLs for the uploaded files.
        """
        logger.info(f"Uploading files in directory '{directory_path}' to Azure Blob Storage container '{container_name}'")
        blob_urls = []
        try:
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                if os.path.isfile(file_path):
                    blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=filename)

                    with open(file_path, "rb") as data:
                        blob_client.upload_blob(data, overwrite=True)
                    logger.info(f"Uploaded file '{filename}' to blob container '{container_name}'")

                    blob_urls.append(blob_client.url)
        except Exception as e:
            logger.error(f"Error uploading files to Blob Storage: {e}")
            raise
        return blob_urls

    def create_batch_pool(self, pool_id, vm_size="STANDARD_D2_V2", dedicated_nodes=1):
        """
        Creates a pool in Azure Batch for processing tasks.

        Args:
            pool_id (str): ID of the pool to create.
            vm_size (str): Size of the virtual machines in the pool. Defaults to "STANDARD_D2_V2".
            dedicated_nodes (int): Number of dedicated compute nodes. Defaults to 1.

        Returns:
            PoolAddParameter: The created pool.
        """
        logger.info(f"Creating Azure Batch pool '{pool_id}' with VM size '{vm_size}' and {dedicated_nodes} dedicated nodes.")
        try:
            pool = PoolAddParameter(
                id=pool_id,
                vm_size=vm_size,
                virtual_machine_configuration=VirtualMachineConfiguration(
                    image_reference={
                        "publisher": "Canonical",
                        "offer": "UbuntuServer",
                        "sku": "18.04-LTS",
                    },
                    node_agent_sku_id="batch.node.ubuntu 18.04",
                ),
                target_dedicated_nodes=dedicated_nodes,
            )
            self.batch_client.pool.add(pool)
            logger.info(f"Azure Batch pool '{pool_id}' created successfully.")
            return pool
        except Exception as e:
            logger.error(f"Error creating Azure Batch pool: {e}")
            raise

    def submit_batch_job(self, pool_id, job_id, task_commands):
        """
        Submits a batch job to Azure Batch.

        Args:
            pool_id (str): The ID of the pool to execute the job.
            job_id (str): The ID of the job.
            task_commands (list): List of task commands to execute as part of the job.

        Returns:
            str: ID of the submitted job.
        """
        logger.info(f"Submitting Azure Batch job '{job_id}' to pool '{pool_id}'.")
        try:
            # Add the job
            self.batch_client.job.add(
                job_id=job_id,
                pool_id=pool_id
            )

            # Add tasks to the job
            for index, command in enumerate(task_commands):
                task = TaskAddParameter(
                    id=f"Task{index}",
                    command_line=command
                )
                self.batch_client.task.add(job_id, task)
            logger.info(f"Azure Batch job '{job_id}' submitted successfully with {len(task_commands)} tasks.")
            return job_id
        except Exception as e:
            logger.error(f"Error submitting Azure Batch job: {e}")
            raise


# --- Example Usage ---
if __name__ == "__main__":
    STORAGE_CONNECTION_STRING = "YOUR_AZURE_STORAGE_CONNECTION_STRING"
    BATCH_ACCOUNT_NAME = "YOUR_BATCH_ACCOUNT_NAME"
    BATCH_ACCOUNT_URL = "https://YOUR_BATCH_ACCOUNT_REGION.batch.azure.com"

    processor = AzureBatchProcessor(
        storage_connection_string=STORAGE_CONNECTION_STRING,
        batch_account_name=BATCH_ACCOUNT_NAME,
        batch_account_url=BATCH_ACCOUNT_URL
    )

    # Example: Upload files to Azure Blob Storage
    local_directory = "media_files"
    container_name = "media-container"
    uploaded_files = processor.upload_files_to_blob(container_name, local_directory)
    print("\n--- Uploaded Files ---")
    print(uploaded_files)

    # Example: Create a Batch pool
    pool_id = "media-processing-pool"
    processor.create_batch_pool(pool_id)

    # Example: Submit a Batch job
    job_id = "media-processing-job"
    commands = [
        "/bin/bash -c 'echo Processing media file 1'",
        "/bin/bash -c 'echo Processing media file 2'"
    ]
    processor.submit_batch_job(pool_id, job_id, commands)
