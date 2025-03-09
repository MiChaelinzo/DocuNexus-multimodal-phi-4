"""
Azure-enabled module for editing and managing media metadata within DocuNexus AGI-Agent.
This module uses libraries for local metadata manipulation and integrates with Azure Blob Storage for file storage.
"""

import os
import tempfile
from azure.storage.blob import BlobServiceClient
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, COMM, TDRC  # For MP3 metadata
from PIL import Image, ExifTags
from src.utils.logger import logger  # Import logger


class AzureMetadataEditor:
    def __init__(self, storage_connection_string):
        """
        Initializes AzureMetadataEditor with Azure Blob Storage.

        Args:
            storage_connection_string (str): Azure Blob Storage connection string.
        """
        self.blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
        logger.info("AzureMetadataEditor initialized with Azure Blob Storage.")

    def upload_to_blob(self, container_name, file_path):
        """
        Uploads a file to an Azure Blob Storage container.

        Args:
            container_name (str): Name of the blob storage container.
            file_path (str): Path to the file to upload.

        Returns:
            str: URL of the uploaded blob.
        """
        logger.info(f"Uploading file to Azure Blob Storage: {file_path}")
        blob_name = os.path.basename(file_path)
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        logger.info(f"File uploaded successfully: {blob_name}")

        return blob_client.url

    def edit_mp3_metadata(self, file_path, title=None, artist=None, album=None, genre=None, comment=None, year=None):
        """
        Edits metadata of an MP3 file.

        Args:
            file_path (str): Path to the MP3 file.
            title (str): Title of the track.
            artist (str): Artist name.
            album (str): Album name.
            genre (str): Genre of the track.
            comment (str): Comments about the track.
            year (str): Release year of the track.

        Returns:
            str: Path to the updated MP3 file.
        """
        logger.info(f"Editing MP3 metadata for file: {file_path}")

        try:
            audio = MP3(file_path, ID3=ID3)

            # Add ID3 tag if not present
            if audio.tags is None:
                audio.add_tags()

            if title:
                audio["TIT2"] = TIT2(encoding=3, text=title)
            if artist:
                audio["TPE1"] = TPE1(encoding=3, text=artist)
            if album:
                audio["TALB"] = TALB(encoding=3, text=album)
            if genre:
                audio["TCON"] = TCON(encoding=3, text=genre)
            if comment:
                audio["COMM"] = COMM(encoding=3, text=comment)
            if year:
                audio["TDRC"] = TDRC(encoding=3, text=year)

            audio.save()
            logger.info(f"MP3 metadata updated successfully: {file_path}")
            return file_path

        except Exception as e:
            logger.error(f"Error updating MP3 metadata: {e}")
            raise

    def edit_image_metadata(self, file_path, updated_metadata):
        """
        Edits EXIF metadata of an image file.

        Args:
            file_path (str): Path to the image file.
            updated_metadata (dict): Dictionary containing metadata to update.

        Returns:
            str: Path to the updated image file.
        """
        logger.info(f"Editing image metadata for file: {file_path}")

        try:
            image = Image.open(file_path)
            exif_data = image.info.get("exif")

            # Update metadata if EXIF exists
            if exif_data:
                for key, value in updated_metadata.items():
                    tag_id = next(
                        (tag for tag, name in ExifTags.TAGS.items() if name == key), None
                    )
                    if tag_id:
                        exif_data[tag_id] = value

            # Save updated image
            updated_file_path = f"updated_{os.path.basename(file_path)}"
            image.save(updated_file_path, exif=exif_data)
            logger.info(f"Image metadata updated successfully: {updated_file_path}")
            return updated_file_path

        except Exception as e:
            logger.error(f"Error updating image metadata: {e}")
            raise


# --- Example Usage ---
if __name__ == "__main__":
    STORAGE_CONNECTION_STRING = "YOUR_AZURE_STORAGE_CONNECTION_STRING"
    CONTAINER_NAME = "media-files"

    editor = AzureMetadataEditor(STORAGE_CONNECTION_STRING)

    # Example: Edit MP3 metadata
    mp3_file_path = "example.mp3"
    updated_mp3 = editor.edit_mp3_metadata(
        mp3_file_path,
        title="New Title",
        artist="New Artist",
        album="New Album",
        genre="Pop",
        comment="This is a test edit.",
        year="2023"
    )
    editor.upload_to_blob(CONTAINER_NAME, updated_mp3)

    # Example: Edit Image metadata
    image_file_path = "example.jpg"
    updated_image = editor.edit_image_metadata(
        image_file_path,
        updated_metadata={"Author": "New Author", "Description": "Updated Description"}
    )
    editor.upload_to_blob(CONTAINER_NAME, updated_image)
