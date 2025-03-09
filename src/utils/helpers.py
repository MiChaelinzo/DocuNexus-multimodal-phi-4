"""
Azure-enabled utility functions and helper classes for DocuNexus AGI-Agent.
Contains general-purpose functions used across different modules.
"""

import streamlit as st
from PIL import Image, ImageOps, ImageDraw
import base64
import json
import pandas as pd  # For DataFrame example in format_response
from azure.storage.blob import BlobServiceClient
import io


def crop_to_circle(image):
    """Crops an image to a circle using PIL."""
    mask = Image.new("L", image.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0) + image.size, fill=255)
    result = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
    result.putalpha(mask)
    return result


def format_response(response_body):
    """Attempts to format a JSON response into a Pandas DataFrame, else returns raw response."""
    try:
        data = json.loads(response_body)
        if isinstance(data, list):
            return pd.DataFrame(data)  # Format JSON list as DataFrame
        else:
            return response_body  # Return raw JSON if not a list
    except json.JSONDecodeError:
        return response_body  # Return raw response if not JSON


def upload_to_blob(container_name, file_path, connection_string):
    """
    Uploads a file to Azure Blob Storage.

    Args:
        container_name (str): The name of the Azure Blob container.
        file_path (str): The path to the file to upload.
        connection_string (str): Azure Blob Storage connection string.

    Returns:
        str: The URL of the uploaded blob.
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_path.split("/")[-1])
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        return blob_client.url
    except Exception as e:
        st.error(f"Error uploading file to Azure Blob Storage: {e}")
        return None


def display_conversation_history(history):
    """Displays the conversation history in Streamlit."""
    st.write("## Neural Link History")  # Example History display title
    if not history:
        st.info("No conversation history yet.")
        return

    human_image = Image.open(io.BytesIO(base64.b64decode(HUMAN_AVATAR_BASE64)))  # Example Avatar - see below for base64
    robot_image = Image.open(io.BytesIO(base64.b64decode(ROBOT_AVATAR_BASE64)))  # Example Avatar - see below for base64
    circular_human_image = crop_to_circle(human_image)  # Circular avatars
    circular_robot_image = crop_to_circle(robot_image)

    for index, chat in enumerate(reversed(history)):  # Reverse history for display order
        col1_q, col2_q = st.columns([1, 11])  # Layout columns for avatar and text
        with col1_q:
            st.image(circular_human_image, width=40)  # Human avatar
        with col2_q:
            st.text_area("You:", value=chat["question"], height=80, key=f"question_{index}", disabled=True)  # Question text area

        col1_a, col2_a = st.columns([1, 11])  # Layout for AGI response
        with col1_a:
            st.image(circular_robot_image, width=40)  # Robot avatar
        with col2_q:
            if isinstance(chat["answer"], pd.DataFrame):  # Handle DataFrame responses specially
                st.dataframe(chat["answer"], key=f"answer_df_{index}")  # Display DataFrame
            else:
                st.text_area("DocuNexus AGI:", value=chat["answer"], height=120, key=f"answer_{index}", disabled=True)  # Answer text area
            if chat["thoughts"]:  # Display thoughts if available
                st.text_area("DocuNexus Thoughts:", value=chat["thoughts"], height=100, key=f"thoughts_{index}", disabled=True)


def display_example_prompts():
    """Displays example prompts in the UI."""
    st.write("## Example Queries")  # Example prompts section title
    example_prompts = [
        "Summarize this PDF document.",
        "Analyze these two documents and compare them.",
        "What objects do you see in this webcam view?",
        "Upload a document to Azure Blob Storage.",
        # ... add more example prompts ...
    ]
    for prompt in example_prompts:
        st.markdown(f"* {prompt}")


# --- Example Avatar Base64 Strings (Placeholders - replace with actual base64 strings) ---
HUMAN_AVATAR_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="  # Placeholder - Replace with actual base64 for human avatar PNG
ROBOT_AVATAR_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="  # Placeholder - Replace with actual base64 for robot avatar PNG
