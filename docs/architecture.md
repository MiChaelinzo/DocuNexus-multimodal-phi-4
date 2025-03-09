+----------------------------------+
|         User (Web Browser)       |
+----------------------------------+
                |
                v
+----------------------------------+
|       Streamlit UI (src/main.py) |
|   - Handles user input/output    |
|   - Displays results and workflows|
+----------------------------------+
                |
                v
+---------------------------------------------+
|      Core AGI Engine (src/core/agi_engine.py)|
|  - Orchestrates AI tasks                    |
|  - Manages interactions with Azure OpenAI  |
|  - Uses PromptTemplates and ResponseFormatter|
+---------------------------------------------+
                |
                v
+---------------------------------------------+
|      Model Manager (src/core/model_manager.py)|
|  - Interacts with Azure AI Inference (Phi-4) |
|  - Provides abstraction for AI model usage  |
|  - Handles API key and endpoint management  |
+---------------------------------------------+
                |
                v
+---------------------------------------------+
|            Azure OpenAI Models              |
|  - Phi-4 Multimodal (text/image tasks)      |
|  - GPT-4 for advanced NLP and reasoning     |
+---------------------------------------------+

Modules:

+---------------------+    +-----------------------+    +---------------------+
| Document Analysis   |    | Media Workflows       |    | Real-Time Communication|
|---------------------|    |-----------------------|    |---------------------|
| - Parsing           |    | - File Conversion    |    | - Webcam/Screen Sharing|
| - Summarization     |    | - Metadata Editing   |    | - RTC Configurations |
| - Deep Analysis     |    | - Batch Processing   |    | - Audio Handling     |
|---------------------|    |-----------------------|    |---------------------|
+---------------------+    +-----------------------+    +---------------------+

+-------------------------+      +-----------------------+
| Azure Blob Storage      |      | Integrations          |
|-------------------------|      |-----------------------|
| - File Upload/Download  |      | - DocuSign Workflows |
| - Secure File Storage   |      | - Snowflake Queries  |
+-------------------------+      +-----------------------+
