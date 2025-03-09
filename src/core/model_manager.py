# src/core/model_manager.py
"""
Manages AI Model loading, selection, and configuration.
Handles both Azure AI Inference (Phi-4) and Phi-4-multimodal-instruct models.
"""

from azure.ai.inference import ChatCompletionsClient # Illustrative - might not be directly used like this
from azure.core.credentials import AzureKeyCredential # Illustrative

from src.utils.config import AppConfig # For loading API keys, model names etc.
from src.utils.logger import logger


class ModelManager:
    def __init__(self):
        self.config = AppConfig() # Load configurations from utils/config.py
        self.Phi-4-multimodal-instruct_model = self._load_Phi-4-multimodal-instruct_model()
        self.phi4_model_client = self._load_phi4_model() # Client, not the raw model itself.

        logger.info("ModelManager initialized, models loaded.")


    def _load_Phi-4-multimodal-instruct_model(self):
        """Loads and configures the Phi-4-multimodal-instruct model (e.g., Phi-4-multimodal-instruct-pro)."""
        try:
            genai.configure(api_key=self.config.Phi-4-multimodal-instruct_api_key) # Load API Key from config
            generation_config = { # Example config
                "temperature": 0.7,
                "top_p": 0.95,
                "max_output_tokens": 8192
            }
            Phi-4-multimodal-instruct_model = genai.GenerativeModel(
                model_name=self.config.Phi-4-multimodal-instruct_model_name, # Model name from config
                generation_config=generation_config,
                system_instruction=self.config.system_instruction  # System instruction from config
            )
            logger.info(f"Phi-4-multimodal-instruct model '{self.config.Phi-4-multimodal-instruct_model_name}' loaded successfully.")
            return Phi-4-multimodal-instruct_model
        except Exception as e:
            logger.error(f"Error loading Phi-4-multimodal-instruct model: {e}")
            return None


    def _load_phi4_model(self):
        """Initializes the Azure AI Inference client for Phi-4."""
        try:
            phi_client = ChatCompletionsClient( # Azure AI Inference client
                endpoint=self.config.azure_endpoint, # Endpoint from config
                credential=AzureKeyCredential(self.config.azure_api_key), # API key from config
            )
            logger.info("Azure AI Inference client (Phi-4 ready) initialized.")
            return phi_client
        except Exception as e:
            logger.error(f"Error initializing Azure AI Inference client: {e}")
            return None


    def get_model(self, use_phi4=False):
        """Returns the appropriate AI model (Phi-4-multimodal-instruct or Phi-4) based on the 'use_phi4' flag."""
        if use_phi4 and self.phi4_model_client: # Check if Phi-4 requested AND client is available
            logger.debug("Returning Phi-4 model client.")
            return self.phi4_model_client # Return the Azure AI Inference Client (for Phi-4 interactions)
        else:
            logger.debug("Returning Phi-4-multimodal-instruct model.")
            return self.Phi-4-multimodal-instruct_model # Default to Phi-4-multimodal-instruct model


    def get_vision_model(self):
        """Returns the Phi-4-multimodal-instruct Vision model (e.g., Phi-4-multimodal-instruct-pro-vision)."""
        logger.debug("Returning Phi-4-multimodal-instruct Vision model.")
        return self.Phi-4-multimodal-instruct_model # In this simplified example, reusing Phi-4-multimodal-instruct_model for vision too


    def get_model_name(self, use_phi4=False):
        """Returns the name of the currently selected model for logging/traceability."""
        if use_phi4 and self.phi4_model_client:
            return self.config.azure_model_name # Model name from config (e.g., "Phi-4-multimodal-instruct")
        else:
            return self.config.Phi-4-multimodal-instruct_model_name # Phi-4-multimodal-instruct model name from config (e.g., "Phi-4-multimodal-instruct-pro")


# --- Example Usage (outside of class definition) ---
if __name__ == "__main__":
    manager = ModelManager()
    Phi-4-multimodal-instruct = manager.get_model()
    phi4_client = manager.get_model(use_phi4=True)

    print(f"Phi-4-multimodal-instruct Model: {Phi-4-multimodal-instruct}") # Print object details (not actual model output here)
    print(f"Phi-4 Client: {phi4_client}") # Print client object
