"""
Azure-enabled configuration management for DocuNexus AGI-Agent.
Handles secure loading of API keys, model names, and other settings from Azure Key Vault or environment variables.
"""

import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from src.utils.logger import logger  # Import logger


class AppConfig:
    def __init__(self, use_key_vault=False, key_vault_name=None):
        """
        Initializes the AppConfig class, optionally integrating with Azure Key Vault.

        Args:
            use_key_vault (bool): Whether to use Azure Key Vault for managing secrets.
            key_vault_name (str, optional): Name of the Azure Key Vault (if use_key_vault is True).
        """
        self.use_key_vault = use_key_vault
        self.key_vault_client = None

        if self.use_key_vault and key_vault_name:
            try:
                self.key_vault_client = SecretClient(
                    vault_url=f"https://{key_vault_name}.vault.azure.net/",
                    credential=DefaultAzureCredential()
                )
                logger.info("Azure Key Vault client initialized.")
            except Exception as e:
                logger.error(f"Error initializing Azure Key Vault client: {e}")
                raise

        # Load configuration
        self._load_config()

    def _get_secret(self, secret_name):
        """
        Retrieves a secret from Azure Key Vault or environment variables as fallback.

        Args:
            secret_name (str): Name of the secret.

        Returns:
            str: Secret value.
        """
        if self.key_vault_client:
            try:
                secret = self.key_vault_client.get_secret(secret_name)
                logger.info(f"Secret '{secret_name}' retrieved successfully from Azure Key Vault.")
                return secret.value
            except Exception as e:
                logger.error(f"Error retrieving secret '{secret_name}' from Azure Key Vault: {e}")

        # Fallback to environment variable
        logger.warning(f"Falling back to environment variable for secret '{secret_name}'.")
        return os.environ.get(secret_name)

    def _load_config(self):
        """
        Loads configuration values securely from Azure Key Vault or environment variables.
        """
        # --- API Keys ---
        self.Phi-4-multimodal-instruct_api_key = self._get_secret("Phi-4-multimodal-instruct_API_KEY")
        if not self.Phi-4-multimodal-instruct_api_key:
            raise ValueError("Phi-4-multimodal-instruct_API_KEY not set in Azure Key Vault or environment variables.")

        self.azure_api_key = self._get_secret("AZURE_AI_API_KEY")
        if not self.azure_api_key:
            raise ValueError("AZURE_AI_API_KEY not set in Azure Key Vault or environment variables.")

        self.docusign_api_key = self._get_secret("DOCUSIGN_API_KEY")

        self.snowflake_credentials = {
            "user": self._get_secret("SNOWFLAKE_USER"),
            "password": self._get_secret("SNOWFLAKE_PASSWORD"),
            "account": self._get_secret("SNOWFLAKE_ACCOUNT"),
            "warehouse": self._get_secret("SNOWFLAKE_WAREHOUSE"),
            "database": self._get_secret("SNOWFLAKE_DATABASE"),
            "schema": self._get_secret("SNOWFLAKE_SCHEMA"),
        }

        # --- Model Names & Endpoints ---
        self.Phi-4-multimodal-instruct_model_name = os.environ.get("Phi-4-multimodal-instruct_MODEL_NAME", "Phi-4-multimodal-instruct-pro")
        self.azure_endpoint = os.environ.get("AZURE_ENDPOINT", "https://models.inference.ai.azure.com")
        self.azure_model_name = os.environ.get("AZURE_MODEL_NAME", "Phi-4-multimodal-instruct")

        # --- System Instruction ---
        self.system_instruction = """
            **Identity & Core Purpose**
            I am DocuNexus, a helpful and informative AGI designed to assist users...
            (This instruction can be expanded based on your application needs.)
        """
        logger.info("Configuration loaded successfully.")


# --- Example Usage ---
if __name__ == "__main__":
    try:
        # Replace with your Azure Key Vault name if Key Vault is being used
        USE_KEY_VAULT = True
        KEY_VAULT_NAME = "your-key-vault-name"

        config = AppConfig(use_key_vault=USE_KEY_VAULT, key_vault_name=KEY_VAULT_NAME)
        print("\n--- DocuNexus Configuration Loaded ---")
        print("Phi-4-multimodal-instruct Model Name:", config.Phi-4-multimodal-instruct_model_name)
        print("Azure AI Endpoint:", config.azure_endpoint)
        print("DocuSign API Key (first 4 chars):", config.docusign_api_key[:4] if config.docusign_api_key else "Not Set")
        print("Snowflake User:", config.snowflake_credentials["user"])
        # ... (print other config details as needed) ...

    except ValueError as e:
        print(f"\n--- Configuration Error ---")
        print(e)
        print("\n**Please ensure Azure Key Vault secrets or environment variables are set correctly.**")
