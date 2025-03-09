"""
Azure-enabled module for handling audio input and output (including Text-to-Speech)
for DocuNexus AGI-Agent.
"""

from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioDataStream, ResultReason
from azure.storage.blob import BlobServiceClient
from pydub import AudioSegment  # For audio file handling (example)
from pydub.playback import play  # For audio playback (example - local playback)
import os  # For temporary file handling
from src.utils.logger import logger  # Import logger


class AzureAudioHandler:
    def __init__(self, azure_speech_key, azure_speech_region, storage_connection_string=None):
        """
        Initializes AzureAudioHandler with Azure Speech Services and optional Blob Storage.

        Args:
            azure_speech_key (str): Azure Speech Service API key.
            azure_speech_region (str): Azure Speech Service region.
            storage_connection_string (str, optional): Azure Blob Storage connection string.
        """
        self.speech_config = SpeechConfig(subscription=azure_speech_key, region=azure_speech_region)
        self.blob_service_client = None
        if storage_connection_string:
            self.blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
            logger.info("Azure Blob Storage integrated.")
        logger.info("AzureAudioHandler initialized with Azure Speech Services.")

    def text_to_speech(self, text, language="en-US", voice="en-US-AriaNeural", upload_to_blob=False, blob_container=None):
        """
        Converts text to speech using Azure Text-to-Speech and optionally uploads the result to Azure Blob Storage.

        Args:
            text (str): Text to be converted to speech.
            language (str): Language code (e.g., "en-US").
            voice (str): Azure Neural TTS voice (e.g., "en-US-AriaNeural").
            upload_to_blob (bool): Whether to upload the result to Azure Blob Storage.
            blob_container (str): Blob container name for storage (required if upload_to_blob is True).

        Returns:
            str: Path to the generated audio file or Blob URL (if uploaded).
        """
        logger.debug(f"Converting text to speech (language: {language}, voice: {voice}): {text[:50]}...")  # Log first 50 chars

        try:
            self.speech_config.speech_synthesis_language = language
            self.speech_config.speech_synthesis_voice_name = voice
            synthesizer = SpeechSynthesizer(speech_config=self.speech_config)

            result = synthesizer.speak_text_async(text).get()
            if result.reason == ResultReason.SynthesizingAudioCompleted:
                audio_file = "temp_audio_output.wav"  # Temporary file for audio output
                audio_stream = AudioDataStream(result)
                audio_stream.save_to_wav_file(audio_file)
                logger.info(f"Text-to-speech audio saved to: {audio_file}")

                if upload_to_blob and self.blob_service_client and blob_container:
                    return self._upload_to_blob(audio_file, blob_container)
                return audio_file  # Return local file path if no Blob upload is requested

            else:
                logger.error(f"Speech synthesis failed with reason: {result.reason}")
                return None
        except Exception as e:
            logger.error(f"Error during text-to-speech conversion: {e}")
            return None

    def _upload_to_blob(self, file_path, container_name):
        """
        Uploads a file to an Azure Blob Storage container.

        Args:
            file_path (str): Path to the file to upload.
            container_name (str): Name of the Blob container.

        Returns:
            str: URL of the uploaded Blob.
        """
        logger.info(f"Uploading audio file to Azure Blob Storage: {file_path}")
        try:
            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=os.path.basename(file_path))
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            logger.info(f"File uploaded successfully to Blob Storage: {blob_client.url}")
            return blob_client.url
        except Exception as e:
            logger.error(f"Error uploading file to Azure Blob Storage: {e}")
            return None

    def play_audio_file(self, audio_filepath):
        """Plays an audio file (example - local playback using pydub)."""
        logger.debug(f"Playing audio file: {audio_filepath}")
        try:
            audio = AudioSegment.from_file(audio_filepath)  # Automatically detect file type
            play(audio)  # Local playback
            logger.info(f"Audio file playback finished: {audio_filepath}")
        except Exception as e:
            logger.error(f"Error playing audio file: {e}")


# --- Example Usage ---
if __name__ == "__main__":
    AZURE_SPEECH_KEY = "YOUR_AZURE_SPEECH_SERVICE_KEY"
    AZURE_SPEECH_REGION = "YOUR_AZURE_REGION"
    STORAGE_CONNECTION_STRING = "YOUR_AZURE_STORAGE_CONNECTION_STRING"

    handler = AzureAudioHandler(
        azure_speech_key=AZURE_SPEECH_KEY,
        azure_speech_region=AZURE_SPEECH_REGION,
        storage_connection_string=STORAGE_CONNECTION_STRING
    )

    # Text-to-Speech Example
    sample_text = "Hello, this is a test of DocuNexus AGI's text-to-speech capability using Azure Speech Services."
    audio_file_or_url = handler.text_to_speech(
        text=sample_text,
        language="en-US",
        voice="en-US-AriaNeural",
        upload_to_blob=True,
        blob_container="audio-files"
    )

    if audio_file_or_url:
        print(f"Audio generated and saved to: {audio_file_or_url}")
        if not audio_file_or_url.startswith("http"):  # If local file path
            handler.play_audio_file(audio_file_or_url)  # Local playback
            os.remove(audio_file_or_url)  # Clean up temp file
