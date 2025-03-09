# DocuNexus AGI-Agent - API Reference (Azure-Focused)

## Core Modules

### 1. `src.core.agi_engine.AGIEngine`

*   **`process_text_request(prompt, context_documents=None, use_phi4=False)`**
    *   **Description:** Processes a text-based user request, leveraging Azure OpenAI models for response generation.
    *   **Parameters:**
        *   `prompt` (str): User's text prompt.
        *   `context_documents` (list[str], optional): List of document texts for context.
        *   `use_phi4` (bool, optional): If True, forces the usage of the Phi-4 model; otherwise, defaults to Azure GPT-4.
    *   **Returns:** `tuple[str, str]`: (formatted_response_text, thoughts_text) - AI-generated response and reasoning process.

*   **`process_vision_request(prompt, image_data)`**
    *   **Description:** Processes a vision-based request, analyzing image data using Azure OpenAI's multimodal model (e.g., Phi-4).
    *   **Parameters:**
        *   `prompt` (str): User's prompt or question about the image view.
        *   `image_data` (bytes): Encoded image data (e.g., JPEG bytes).
    *   **Returns:** `tuple[str, str]`: (formatted_response_text, thoughts_text) - AI analysis response and thought process.

---

### 2. `src.core.model_manager.ModelManager`

*   **`get_model(use_phi4=False)`**
    *   **Description:** Returns the appropriate Azure OpenAI model instance based on the `use_phi4` flag.
    *   **Parameters:**
        *   `use_phi4` (bool, optional): If True, returns the Phi-4 multimodal model; otherwise, defaults to Azure GPT-4.
    *   **Returns:** `ChatCompletionsClient`: Azure OpenAI Client instance.

*   **`get_vision_model()`**
    *   **Description:** Returns the Azure OpenAI Phi-4 multimodal model instance.
    *   **Returns:** `ChatCompletionsClient`: Azure OpenAI Phi-4 model instance for vision-related tasks.

---

### 3. `src.document_analysis` Module

*   **`summarize_document(text, summary_length="concise")`**
    *   **Description:** Summarizes the provided text using Azure OpenAI models.
    *   **Parameters:**
        *   `text` (str): The document text to summarize.
        *   `summary_length` (str, optional): Summary length, e.g., "concise", "detailed", or "comprehensive".
    *   **Returns:** `str`: The summarized text.

*   **`extract_metadata(file_path)`**
    *   **Description:** Extracts metadata from documents (e.g., PDFs, DOCX) using Azure Cognitive Services.
    *   **Parameters:**
        *   `file_path` (str): Path to the document file.
    *   **Returns:** `dict`: Extracted metadata, including title, author, and creation/modification dates.

---

### 4. `src.media_workflows` Module

*   **`convert_media(input_file, output_format)`**
    *   **Description:** Converts media files to the specified format using Azure Media Services.
    *   **Parameters:**
        *   `input_file` (str): Path to the input media file.
        *   `output_format` (str): Desired output format (e.g., "mp4", "mp3").
    *   **Returns:** `str`: Path or URL to the converted media file.

*   **`edit_metadata(media_file, metadata_updates)`**
    *   **Description:** Updates metadata for media files.
    *   **Parameters:**
        *   `media_file` (str): Path to the media file.
        *   `metadata_updates` (dict): Key-value pairs of metadata to update.
    *   **Returns:** `bool`: Success status of the update.

---

### 5. `src.real_time_comm` Module

*   **`start_webcam_analysis(prompt)`**
    *   **Description:** Initiates live analysis of webcam feed using Azure OpenAI and Cognitive Services.
    *   **Parameters:**
        *   `prompt` (str): User's instructions for the analysis (e.g., "Identify objects in view").
    *   **Returns:** `tuple[str, str]`: AI response and reasoning.

*   **`start_screen_sharing_analysis(prompt)`**
    *   **Description:** Processes screen-sharing frames and provides insights using Azure OpenAI.
    *   **Parameters:**
        *   `prompt` (str): User's instructions for the analysis.
    *   **Returns:** `tuple[str, str]`: AI analysis and thought process.

---

### 6. `src.integrations` Module

*   **`send_to_docusign(document, recipient_email, recipient_name)`**
    *   **Description:** Sends a document for e-signature using DocuSign's API.
    *   **Parameters:**
        *   `document` (str): Path to the document file.
        *   `recipient_email` (str): Email address of the recipient.
        *   `recipient_name` (str): Name of the recipient.
    *   **Returns:** `dict`: Response from DocuSign API.

*   **`execute_snowflake_query(query)`**
    *   **Description:** Executes a SQL query on a Snowflake database.
    *   **Parameters:**
        *   `query` (str): SQL query to execute.
    *   **Returns:** `list`: Query results.

---

## **Example Usage**

### **1. Text-Based Request**
```python
from src.core.agi_engine import AGIEngine

engine = AGIEngine()
response, thoughts = engine.process_text_request(
    "Summarize the key findings in this report.",
    context_documents=["This is an example document text."],
    use_phi4=False  # Use Azure GPT-4 by default
)

print("Response:", response)
print("Thoughts:", thoughts)
```

---

### **2. Vision-Based Request**
```python
from src.core.agi_engine import AGIEngine

engine = AGIEngine()

# Example image data (replace with your actual image bytes)
with open("example_image.jpg", "rb") as image_file:
    image_data = image_file.read()

response, thoughts = engine.process_vision_request(
    "Describe the objects in this image.",
    image_data=image_data
)

print("Response:", response)
print("Thoughts:", thoughts)
```

---

### **3. Media Conversion**
```python
from src.media_workflows.media_converter import convert_media

output_file = convert_media("input_video.mp4", "mov")
print(f"Converted media file available at: {output_file}")
```

---

### **4. Snowflake Query**
```python
from src.integrations.snowflake_api import execute_snowflake_query

query = "SELECT * FROM employees WHERE department = 'Engineering';"
results = execute_snowflake_query(query)

print("Query Results:", results)
```

---

## **Azure-Centric Features**
1. **Azure OpenAI Services:** Uses GPT-4 and Phi-4 models for text and multimodal tasks.
2. **Azure Cognitive Services:** Handles vision, speech, and document processing tasks.
3. **Azure Media Services:** Powers media transcoding and optimization workflows.
4. **Azure Blob Storage:** Stores and retrieves processed files securely.
5. **Azure Key Vault:** Manages API keys and sensitive credentials securely.

This Azure-focused API reference ensures streamlined integration with Azure services while offering powerful AI-driven functionalities. Let me know if additional details are needed! 🚀
