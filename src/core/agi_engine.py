# src/core/agi_engine.py
"""
Core AGI Engine for DocuNexus. Orchestrates model interactions,
reasoning flow, and overall AI task management.
"""

from src.core.model_manager import ModelManager
from src.core.prompt_templates import PromptTemplates
from src.core.response_formatter import ResponseFormatter
from src.utils.logger import logger
import base64  # Import for vision request example


class AGIEngine:
    def __init__(self):
        self.model_manager = ModelManager()
        self.prompt_templates = PromptTemplates()
        self.response_formatter = ResponseFormatter()
        logger.info("AGIEngine initialized.")

    def process_text_request(self, prompt, context_documents=None, use_phi4=False):
        """Processes text-based requests using the AGI model."""
        logger.info(f"Processing text request: {prompt[:50]}...") # Log only first 50 chars

        # 1. Select Model (Phi-4 or Phi-4-multimodal-instruct based on use_phi4 flag or default logic)
        model = self.model_manager.get_model(use_phi4=use_phi4)
        model_name = self.model_manager.get_model_name(use_phi4=use_phi4)  # Get model name

        # 2. Generate Prompt using Prompt Templates (based on task type)
        full_prompt = self.prompt_templates.create_prompt("document_analysis", prompt, context=context_documents) # Example template

        # 3. Call Azure AI Inference (or Phi-4-multimodal-instruct) Model for Response Generation
        try:
            logger.info(f"Calling AI model: {model_name}") # Log model call
            ai_response = model.generate_content(contents=full_prompt) #  Using GenerativeModel interface (for both Phi-4-multimodal-instruct/Phi-4)
            response_text = ai_response.text # Assuming consistent response structure
            logger.info(f"AI response received (first 100 chars): {response_text[:100]}...")

        except Exception as e:
            logger.error(f"Error from AI Model: {e}")
            return f"Error processing request with AI model: {e}"

        # 4. Format and Structure Response
        formatted_response, thoughts = self.response_formatter.format_text_response(response_text) # Example formatting

        return formatted_response, thoughts


    def process_vision_request(self, prompt, image_data):
        """Processes vision-based requests using the Vision AGI model (Phi-4-multimodal-instruct Vision in this example)."""
        logger.info("Processing vision request...")

        vision_model = self.model_manager.get_vision_model() # Assumes ModelManager handles vision model retrieval

        contents = [
            {
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(image_data).decode()}} # Example image part
                ]
            }
        ]

        try:
            logger.info("Calling Vision AI model (Phi-4-multimodal-instruct Vision)")
            ai_response = vision_model.generate_content(contents=contents) # Call vision model
            response_text = ai_response.text
            logger.info(f"Vision AI response received (first 100 chars): {response_text[:100]}...")

        except Exception as e:
            logger.error(f"Error from Vision AI Model: {e}")
            return f"Error processing vision request: {e}", None # Return error and no thoughts

        formatted_response, thoughts = self.response_formatter.format_text_response(response_text) # Format response

        return formatted_response, thoughts


# --- Example of how AGIEngine might be used (not part of class definition) ---
if __name__ == "__main__":
    engine = AGIEngine()
    sample_prompt = "Summarize the key points of a contract about data privacy."
    response, thoughts = engine.process_text_request(sample_prompt)

    print("\n--- DocuNexus AGI Response ---")
    print(response)
    if thoughts:
        print("\n--- DocuNexus Thoughts ---")
        print(thoughts)
