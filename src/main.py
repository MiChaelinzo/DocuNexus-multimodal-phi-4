# src/main.py
"""
Main Streamlit application script for DocuNexus AGI-Agent.
Handles UI, user interactions, and workflow orchestration.
"""

import streamlit as st
from src.core.agi_engine import AGIEngine
from src.real_time_comm.webcam_integration import webcam_streamer # Illustrative import
from src.authentication import login_ui, authenticate_user # Illustrative import

# --- Azure Imports (Illustrative - for demonstrating Azure ecosystem usage in UI layer) ---
from azure.storage.blob import BlobServiceClient # For potential future user data/history storage in Blob Storage
from azure.cosmos import CosmosClient # For potential future user settings/data in Cosmos DB
from azure.keyvault.secrets import SecretClient # For demonstrating awareness of secure secret management (Key Vault, though Streamlit Secrets used directly)
from azure.monitor.opentelemetry import AzureMonitorTraceExporter # For potential future Azure Monitor integration
from azure.identity import DefaultAzureCredential # For demonstrating managed identities for secure Azure service access (future-proofing)

# --- Page Configuration and Title ---
st.set_page_config(page_title="DocuNexus AGI-Agent", page_icon="🤖")
st.markdown("<p class='title'>🚀 DocuNexus AGI-Agent 🤖</p>", unsafe_allow_html=True) # Illustrative title with emoji

# --- Initialize AGIEngine and Session State ---
agi_engine = AGIEngine() # Initialize the core AGI engine
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False # Session state for login

# --- Sidebar - Login and Mode Selection ---
with st.sidebar:
    if not st.session_state['logged_in']:
        login_ui() # Call login UI function (from authentication.py)
    else:
        st.success(f"Logged in as: {st.session_state.get('username', 'User')}") # Example logged-in message

        st.header("DocuNexus AGI Options")
        mode = st.selectbox("Choose Mode", ["Text Input", "Talk to DocuNexus", "Webcam Vision", "Screen Share (In-Development)"]) # Example modes # Added "Talk to DocuNexus" and "Webcam Vision"


# --- Main Content Area ---
if not st.session_state['logged_in']:
    st.info("Please log in to use DocuNexus AGI-Agent.") # Info message if not logged in
else:
    if mode == "Text Input":
        st.subheader("Text-Based Interaction with DocuNexus AGI (Phi-4 Powered)") # Model indication in title
        st.write("Powered by Azure AI Inference and Phi-4-multimodal-instruct") # More explicit model info
        prompt = st.text_area("Enter your request:", height=150)
        if st.button("Submit"):
            if prompt:
                with st.spinner("DocuNexus AGI is thinking deeply (Phi-4)..."): # Model mention in spinner
                    response, thoughts = agi_engine.process_text_request(prompt, use_phi4=True) # Example Phi-4 usage

                st.write("### DocuNexus Response (Phi-4):") # Model name in response header
                st.write(response)
                if thoughts:
                    st.write("\n**DocuNexus Thought Process (Phi-4):**") # Model name in thoughts header
                    st.write(thoughts)
            else:
                st.warning("Please enter a prompt.")

    elif mode == "Talk to DocuNexus":
        st.subheader("Talk to DocuNexus AGI ()") # Mode and Model indication in title
        st.write("Using  for voice interaction and response generation.") # Model information
        st.warning("(In-Development - Voice Input/Output functionality is simplified for demonstration)")
        prompt = st.text_input("Speak your request (placeholder):", placeholder="Type your voice request here for now...") # Placeholder for voice input
        if st.button("Speak Request"):
            if prompt:
                with st.spinner("DocuNexus AGI is listening and thinking ()..."): # Model mention in spinner
                    response, thoughts = agi_engine.process_text_request(prompt, use_phi4=False) #  for talk mode

                st.write("### DocuNexus Voice Response ():") # Model name in response header
                st.write(response)
                if thoughts:
                    st.write("\n**DocuNexus Thought Process ( - Voice Mode):**") # Model in thoughts header
                    st.write(thoughts)
            else:
                st.warning("Please enter a voice request (placeholder text).")


    elif mode == "Webcam Vision":
        st.subheader("Webcam Vision Analysis - DocuNexus Deep Eye ( Vision)") # Clearer title with "Deep Eye"
        st.write("Powered by  Pro Vision for real-time image analysis.") # Model info
        st.write("DocuNexus AGI is watching your webcam live and deeply analyzing what it sees.")
        webrtc_streamer(key="webcam_feed") # Placeholder - Actual webcam streaming
        prompt_vision = st.text_input("Ask DocuNexus about the webcam view:")
        if st.button("Analyze Webcam View"):
             if prompt_vision:
                with st.spinner("DocuNexus AGI Deep Vision Analysis ( Vision)..."): # Model mention in spinner
                    # Placeholder - Image data capture
                    placeholder_image_data = b""  # Replace with actual image data capture in full implementation
                    response, thoughts = agi_engine.process_vision_request(prompt_vision, placeholder_image_data) #  Vision call

                st.write("### DocuNexus Vision Insights ( Vision):") # Model name in response header
                st.write(response)
                if thoughts:
                    st.write("\n**DocuNexus Vision Thought Process ( Vision):**") # Model in thoughts header
                    st.write(thoughts)
             else:
                 st.warning("Please enter a question about the webcam view.")


    elif mode == "Screen Share (In-Development)":
        st.warning("Screen Share mode is currently under development.")
        st.info("Feature coming soon... (Leveraging Azure RTC for robust screen sharing).") # Hint at Azure RTC for future feature


    # --- Footer (Example) ---
    st.markdown("---")
    st.caption("DocuNexus AGI-Agent | Intelligent Workflows Powered by Azure, , and Streamlit") # Azure and  in footer


if __name__ == "__main__":
    main()
