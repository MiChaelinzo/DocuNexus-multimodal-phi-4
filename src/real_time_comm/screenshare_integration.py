"""
Azure-enabled module for screen sharing integration and processing for DocuNexus AGI-Agent,
using streamlit-webrtc and Azure Cognitive Services.
"""

import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration, WebRtcMode
import av
import cv2
import numpy as np
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from azure.core.credentials import AzureKeyCredential
from src.utils.logger import logger

# Azure Configuration for STUN/TURN servers
RTC_CONFIG = RTCConfiguration({
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
})


class AzureScreenShareProcessor(VideoTransformerBase):
    """
    Video processor for analyzing screen-sharing feed using Azure Cognitive Services.
    """
    def __init__(self, azure_cv_client: ComputerVisionClient):
        """
        Initializes the processor with Azure Cognitive Services client.

        Args:
            azure_cv_client (ComputerVisionClient): Azure Computer Vision client instance.
        """
        self.azure_cv_client = azure_cv_client
        logger.info("AzureScreenShareProcessor initialized with Azure Computer Vision.")

    def transform(self, frame):
        """
        Transforms each frame from the screen-sharing feed by analyzing it with Azure Computer Vision.

        Args:
            frame (av.VideoFrame): Input video frame.

        Returns:
            av.VideoFrame: Annotated video frame with analysis results.
        """
        img = frame.to_ndarray(format="rgb24")  # Convert frame to numpy array

        # Convert frame to a temporary file for Azure Computer Vision processing
        temp_file_path = "temp_screen_frame.jpg"
        cv2.imwrite(temp_file_path, img)

        try:
            # Analyze the image using Azure Computer Vision
            with open(temp_file_path, "rb") as image_stream:
                analysis = self.azure_cv_client.analyze_image_in_stream(
                    image_stream,
                    visual_features=[VisualFeatureTypes.DESCRIPTION, VisualFeatureTypes.TAGS]
                )

            # Annotate frame with description
            description = analysis.description.captions[0].text if analysis.description.captions else "No description available"
            tags = ", ".join(analysis.tags) if analysis.tags else "No tags available"

            annotated_frame = np.copy(img)
            cv2.putText(annotated_frame, f"Description: {description}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"Tags: {tags}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            logger.info("Frame successfully analyzed and annotated.")
            return av.VideoFrame.from_ndarray(annotated_frame, format="rgb24")  # Return annotated frame

        except Exception as e:
            logger.error(f"Error during screen frame analysis: {e}")
            return frame  # Return original frame in case of error

        finally:
            # Clean up temporary file
            try:
                os.remove(temp_file_path)
            except Exception as cleanup_error:
                logger.warning(f"Could not remove temporary file: {cleanup_error}")


def screenshare_streamer(key="docunexus_screenshare", azure_cv_client=None):
    """
    Streamlit component for screen sharing feed with Azure Cognitive Services for vision analysis.

    Args:
        key (str): Streamlit component key for screen sharing.
        azure_cv_client (ComputerVisionClient): Azure Computer Vision client instance.
    """
    if azure_cv_client is None:
        st.error("Azure Computer Vision client instance must be provided to screenshare_streamer.")
        return

    webrtc_ctx = webrtc_streamer(
        key=key,
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIG,
        media_stream_constraints={"video": True, "audio": False},
        video_processor_factory=lambda: AzureScreenShareProcessor(azure_cv_client),
        async_processing=True  # Enable async processing for smoother UI
    )
    return webrtc_ctx


# --- Example Usage ---
if __name__ == "__main__":
    AZURE_CV_ENDPOINT = "YOUR_AZURE_CV_ENDPOINT"
    AZURE_CV_API_KEY = "YOUR_AZURE_CV_API_KEY"

    # Initialize Azure Computer Vision Client
    azure_cv_client = ComputerVisionClient(
        endpoint=AZURE_CV_ENDPOINT,
        credential=AzureKeyCredential(AZURE_CV_API_KEY)
    )

    st.title("Azure Screen Sharing Integration Demo")
    screenshare_streamer(key="azure_screenshare", azure_cv_client=azure_cv_client)
