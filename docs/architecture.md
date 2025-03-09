# DocuNexus AGI-Agent - Architecture Overview

## High-Level Architecture Diagram

[Insert a high-level architecture diagram here - could be a simple text-based diagram or an image if you want to create one.
Example (text-based):
Use code with caution.
Markdown
User (Web Browser)
|
V
Streamlit UI (src/main.py)
|
V (Requests) --------> AGIEngine (src/core/agi_engine.py)
| ^ ^
| | | (Model Calls)
V (Responses) ModelManager (src/core/model_manager.py)
/
/
V V
Azure AI Inference (Phi-4) Gemini Models (Gemini Pro, Vision)

Modules:

Document Analysis (src/document_analysis/)

Media Workflows (src/media_workflows/)

Real-Time Communication (src/real_time_comm/)

Integrations (src/integrations/)

Utilities (src/utils/)

]

## Component Breakdown

*   **Streamlit UI (`src/main.py`):**
    *   Serves as the user interface, handling user input and displaying results.
    *   Orchestrates workflows by calling the `AGIEngine`.
    *   Manages session state and user login.
    *   Integrates webcam and screen sharing components.

*   **Core AGI Engine (`src/core/agi_engine.py`):**
    *   The central orchestrator of DocuNexus AGI's intelligence.
    *   Manages interactions with different AI models via the `ModelManager`.
    *   Implements the main processing logic for text and vision requests.
    *   Utilizes `PromptTemplates` for prompt generation and `ResponseFormatter` for output structuring.

*   **Model Manager (`src/core/model_manager.py`):**
    *   Responsible for loading, configuring, and selecting AI models: Azure AI Inference (Phi-4) and Gemini models.
    *   Abstracts model-specific API calls, providing a consistent interface to the `AGIEngine`.
    *   Handles API key management (configuration).

*   **Document Analysis Module (`src/document_analysis/`):**
    *   Contains modules for document parsing (`document_parser.py`), summarization (`summarizer.py`), deep analysis (`analyzer.py`), and metadata handling (`metadata_handler.py`).
    *   Provides functionalities for extracting insights and information from various document formats.

*   **Media Workflows Module (`src/media_workflows/`):**
    *   Includes modules for media conversion (`media_converter.py`), metadata editing (`metadata_editor.py`), content analysis (`content_analyzer.py`), and batch processing (`batch_processor.py`).
    *   Automates and streamlines common media-related tasks.

*   **Real-Time Communication Module (`src/real_time_comm/`):**
    *   Manages webcam integration (`webcam_integration.py`), screen sharing (`screenshare_integration.py`), RTC configurations (`rtc_manager.py`), and audio handling (`audio_handler.py`).
    *   Enables live video and audio features powered by WebRTC and potentially Azure Communication Services.

*   **Integrations Module (`src/integrations/`):**
    *   Houses integrations with external services like DocuSign (`docusign_api.py`) and Snowflake (`snowflake_api.py`).
    *   Allows DocuNexus AGI to connect to and leverage other platforms for enhanced workflows.

*   **Utilities Module (`src/utils/`):**
    *   Provides utility functions and configurations used across the application, such as configuration loading (`config.py`), helper functions (`helpers.py`), and logging (`logger.py`).

## Technology Stack

*   **AI Models:** Microsoft Azure AI Inference (Phi-4-multimodal-instruct), Google Gemini Pro, Gemini Pro Vision.
*   **Cloud Platform:** Microsoft Azure (for potential deployment, scalability, and Azure AI Inference).
*   **UI Framework:** Streamlit (for rapid development of interactive web application).
*   **Real-Time Communication:** WebRTC (via streamlit-webrtc), potentially Azure Communication Services (for future expansion).
*   **Text-to-Speech:** gTTS (Google Text-to-Speech).
*   **Document Parsing Libraries:** pypdf, python-docx.
*   **Media Libraries:** MoviePy, Pillow, pydub, SpeechRecognition.
*   **Programming Language:** Python.

## Scalability & Future Directions

[Section discussing scalability considerations using Azure and planned future features (as mentioned in previous responses).]
