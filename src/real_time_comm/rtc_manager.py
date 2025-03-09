# src/real_time_comm/audio_handler.py
"""
Handles audio input and output (including Text-to-Speech)
for DocuNexus AGI-Agent.
"""

from gtts import gTTS # For Text-to-Speech
from pydub import AudioSegment # For audio file handling (example)
from pydub.playback import play # For audio playback (example - local playback)
import os # For temporary file handling
from src.utils.logger import logger # Import logger

class AudioHandler:
    def __init__(self):
        logger.info("AudioHandler initialized.")

    def text_to_speech(self, text, language="en"):
        """
        Converts text to speech using gTTS (Google Text-to-Speech).
        """
        logger.debug(f"Converting text to speech (language: {language}): {text[:50]}...") # Log first 50 chars

        try:
            tts = gTTS(text=text, lang=language)
            audio_file = "temp_audio_output.mp3" # Temporary file - better to use tempfile module in real app
            tts.save(audio_file)
            logger.info(f"Text-to-speech audio saved to: {audio_file}")
            return audio_file # Return filepath to audio file

        except Exception as e:
            logger.error(f"Error during text-to-speech conversion: {e}")
            return None


    def play_audio_file(self, audio_filepath):
        """Plays an audio file (example - local playback using pydub)."""
        logger.debug(f"Playing audio file: {audio_filepath}")
        try:
            audio = AudioSegment.from_mp3(audio_filepath) # Example - assumes MP3
            play(audio) # Local playback - Streamlit frontend audio component is usually preferred for web apps
            logger.info(f"Audio file playback finished: {audio_filepath}")
        except Exception as e:
            logger.error(f"Error playing audio file: {e}")


# --- Example Usage (outside class definition) ---
if __name__ == "__main__":
    handler = AudioHandler()
    sample_text = "Hello, this is a test of DocuNexus AGI's text-to-speech capability."
    audio_file = handler.text_to_speech(sample_text)

    if audio_file:
        print(f"\nAudio file generated: {audio_file}. Playing audio (locally)...")
        handler.play_audio_file(audio_file) # Example local playback
        os.remove(audio_file) # Clean up temp file
