# src/main.py
"""
Main Streamlit application script for DocuNexus AGI-Agent.
Handles UI, user interactions, and workflow orchestration.
"""

import streamlit as st
from src.core.agi_engine import AGIEngine
from src.real_time_comm.webcam_integration import webrtc_streamer # Illustrative import
from src.authentication import login_ui, authenticate_user # Illustrative import
from src.utils.helpers import display_conversation_history, display_example_prompts # Example utility functions
from src.integrations.docusign_api import send_to_docusign # Example integration import

# --- Azure Imports (Illustrative - for demonstrating Azure ecosystem usage in UI layer) ---
from azure.storage.blob import BlobServiceClient # For potential future user data/history storage in Blob Storage
from azure.cosmos import CosmosClient # For potential future user settings/data in Cosmos DB
from azure.keyvault.secrets import SecretClient # For demonstrating awareness of secure secret management (Key Vault, though Streamlit Secrets used directly)
from azure.monitor.opentelemetry import AzureMonitorTraceExporter # For potential future Azure Monitor integration
from azure.identity import DefaultAzureCredential # For demonstrating managed identities for secure Azure service access (future-proofing)


# --- Page Configuration and Title ---
st.set_page_config(page_title="DocuNexus AGI-Agent", page_icon="🤖", layout="wide") # Wide layout for better display
st.markdown("<p class='title'>🚀 DocuNexus AGI-Agent 🤖</p>", unsafe_allow_html=True) # Illustrative title with emoji

# --- Initialize AGIEngine and Session State ---
agi_engine = AGIEngine() # Initialize the core AGI engine
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False # Session state for login
if "history" not in st.session_state:
    st.session_state["history"] = [] # Initialize chat history


# --- Sidebar - Login, CyberMatrix Status, Integrations ---
with st.sidebar:
    login_ui() # Call login UI function (from authentication.py)
    st.markdown("---") # Separator after login

    st.sidebar.markdown( # CyberMatrix Status - illustrative
    """
    <h3 style='font-size: 22px; font-family: Orbitron, sans-serif; color: #00ffbf; text-shadow: 0 0 15px #00ffff, 0 0 30px #00ffff, 0 0 45px #00ffff, 0 0 60px #00ffff; animation: flicker-fast 1s infinite, glitch-slow 2s infinite;'>CyberMatrix Status</h3>
    """,
    unsafe_allow_html=True
)
    st.markdown("- CPU: 67%") # Example metrics
    st.markdown("- RAM: 34GB / 128GB")
    st.markdown("- Network: Online")
    st.markdown("- AGI Core: Active")
    st.markdown("---")  # Separator

    st.header("Integrations") # Example Integrations in Sidebar
    st.subheader("DocuSign")
    docusign_button = st.button("Send to DocuSign (Placeholder - Not Functional)") # Placeholder button
    st.subheader("Snowflake")
    snowflake_query_button = st.button("Execute Snowflake Query (Placeholder - Not Functional)") # Placeholder button

    st.markdown("---")
    logout_button = st.button("Logout") # Logout button in sidebar
    if logout_button:
        st.session_state['logged_in'] = False
        st.session_state["history"].clear()  # Clear history on logout
        st.rerun()


    st.header("DocuNexus AGI Options")
    mode = st.selectbox("Choose Mode", ["Text Input", "Talk to DocuNexus", "Webcam Vision", "Screen Share (In-Development)"]) # Example modes


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
                st.text_area("", value=response, height=200) # Using text_area for response display
                if thoughts:
                    st.write("\n**DocuNexus Thought Process (Phi-4):**") # Model name in thoughts header
                    st.text_area("", value=thoughts, height=150)
            else:
                st.warning("Please enter a prompt.")

    elif mode == "Talk to DocuNexus": # Talk to DocuNexus Mode UI
        st.subheader("Talk to DocuNexus AGI (Phi-4-multimodal-instruct)") # Mode and Model indication in title
        st.write("Using Phi-4-multimodal-instruct for voice interaction and response generation.") # Model information
        st.warning("(In-Development - Voice Input/Output functionality is simplified for demonstration)")
        prompt = st.text_input("Speak your request (placeholder):", placeholder="Type your voice request here for now...") # Placeholder for voice input
        if st.button("Speak Request"):
            if prompt:
                with st.spinner("DocuNexus AGI is listening and thinking (Phi-4-multimodal-instruct)..."): # Model mention in spinner
                    response, thoughts = agi_engine.process_text_request(prompt, use_phi4=False) # Phi-4-multimodal-instruct for talk mode

                st.write("### DocuNexus Voice Response (Phi-4-multimodal-instruct):") # Model name in response header
                st.text_area("", value=response, height=200)
                if thoughts:
                    st.write("\n**DocuNexus Thought Process (Phi-4-multimodal-instruct - Voice Mode):**") # Model in thoughts header
                    st.text_area("", value=thoughts, height=150)
            else:
                st.warning("Please enter a voice request (placeholder text).")


    elif mode == "Webcam Vision": # Webcam Vision Mode UI
        st.subheader("Webcam Vision Analysis - DocuNexus Deep Eye (Phi-4-multimodal-instruct Vision)") # Clearer title with "Deep Eye"
        st.write("Powered by Phi-4-multimodal-instruct Pro Vision for real-time image analysis.") # Model info
        st.write("DocuNexus AGI is watching your webcam live and deeply analyzing what it sees.")
        webrtc_streamer(key="webcam_feed") # Placeholder - Actual webcam streaming, replace with real implementation in `webcam_integration.py`
        prompt_vision = st.text_input("Ask DocuNexus about the webcam view:")
        if st.button("Analyze Webcam View"):
             if prompt_vision:
                with st.spinner("DocuNexus AGI Deep Vision Analysis (Phi-4-multimodal-instruct Vision)..."): # Model mention in spinner
                    # Placeholder - Image data capture - replace with actual image capture from webcam
                    placeholder_image_data = b""  # Replace with actual image data capture in full implementation
                    response, thoughts = agi_engine.process_vision_request(prompt_vision, placeholder_image_data) # Phi-4-multimodal-instruct Vision call

                st.write("### DocuNexus Vision Insights (Phi-4-multimodal-instruct Vision):") # Model name in response header
                st.text_area("", value=response, height=200)
                if thoughts:
                    st.write("\n**DocuNexus Vision Thought Process (Phi-4-multimodal-instruct Vision):**") # Model in thoughts header
                    st.text_area("", value=thoughts, height=150)
             else:
                 st.warning("Please enter a question about the webcam view.")


    elif mode == "Screen Share (In-Development)": # Screen Share Mode UI
        st.warning("Screen Share mode is currently under development.")
        st.info("Feature coming soon... (Leveraging Azure RTC for robust screen sharing).") # Hint at Azure RTC

    # --- Conversation History Display (using utility function) ---
    if st.session_state['logged_in']: # Only show history if logged in
        display_conversation_history(st.session_state["history"]) # Call utility function to display history

    # --- Example Prompts Display (using utility function) ---
    display_example_prompts()  # Call utility function to show example prompts


# --- Footer (Example) ---
st.markdown("---")
st.caption("DocuNexus AGI-Agent | Intelligent Workflows Powered by Azure, Phi-4-multimodal-instruct, and Streamlit")
