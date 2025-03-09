"""
Azure-enabled module for integrating with Snowflake for DocuNexus AGI-Agent.
Handles secure Snowflake connection management and query execution with optional Azure Key Vault integration.
"""

import snowflake.connector
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from src.utils.logger import logger  # Import logger


class AzureSnowflakeIntegration:
    def __init__(self, use_key_vault=False, key_vault_name=None):
        """
        Initializes AzureSnowflakeIntegration with optional Azure Key Vault for credential management.

        Args:
            use_key_vault (bool): Whether to use Azure Key Vault for managing secrets.
            key_vault_name (str, optional): Name of the Azure Key Vault (if use_key_vault is True).
        """
        self.use_key_vault = use_key_vault
        self.snowflake_credentials = {}
        self.key_vault_client = None

        if use_key_vault and key_vault_name:
            self.key_vault_client = SecretClient(
                vault_url=f"https://{key_vault_name}.vault.azure.net/",
                credential=DefaultAzureCredential()
            )
            logger.info("Azure Key Vault integration enabled.")
        else:
            logger.warning("Azure Key Vault is not enabled. Using local configuration.")

    def _get_secret_from_key_vault(self, secret_name):
        """
        Retrieves a secret from Azure Key Vault.

        Args:
            secret_name (str): Name of the secret.

        Returns:
            str: Secret value.
        """
        try:
            secret = self.key_vault_client.get_secret(secret_name)
            logger.info(f"Secret '{secret_name}' retrieved successfully from Azure Key Vault.")
            return secret.value
        except Exception as e:
            logger.error(f"Error retrieving secret '{secret_name}' from Azure Key Vault: {e}")
            return None

    def connect_to_snowflake(self):
        """
        Establishes a connection to Snowflake using credentials from Azure Key Vault or local configuration.

        Returns:
            snowflake.connector.connection.SnowflakeConnection: Snowflake connection object.
        """
        try:
            if self.use_key_vault:
                self.snowflake_credentials = {
                    "user": self._get_secret_from_key_vault("snowflake-user"),
                    "password": self._get_secret_from_key_vault("snowflake-password"),
                    "account": self._get_secret_from_key_vault("snowflake-account"),
                    "warehouse": self._get_secret_from_key_vault("snowflake-warehouse"),
                    "database": self._get_secret_from_key_vault("snowflake-database"),
                    "schema": self._get_secret_from_key_vault("snowflake-schema"),
                }
            else:
                # Local configuration fallback
                from src.utils.config import AppConfig
                config = AppConfig()
                self.snowflake_credentials = {
                    "user": config.snowflake_user,
                    "password": config.snowflake_password,
                    "account": config.snowflake_account,
                    "warehouse": config.snowflake_warehouse,
                    "database": config.snowflake_database,
                    "schema": config.snowflake_schema,
                }

            connection = snowflake.connector.connect(**self.snowflake_credentials)
            logger.info("Connected to Snowflake successfully.")
            return connection
        except Exception as e:
            logger.error(f"Error connecting to Snowflake: {e}")
            return None

    def execute_query(self, query):
        """
        Executes a query on Snowflake and fetches the results.

        Args:
            query (str): SQL query to execute.

        Returns:
            list: Query results.
        """
        connection = self.connect_to_snowflake()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query)
                results = cursor.fetchall()
                logger.info("Query executed successfully.")
                return results
            except Exception as e:
                logger.error(f"Error executing query: {e}")
                return None
            finally:
                connection.close()
        else:
            logger.error("Unable to establish a connection to Snowflake.")
            return None


# --- Example Usage ---
if __name__ == "__main__":
    # Optionally, set up Azure Key Vault integration
    USE_KEY_VAULT = True
    KEY_VAULT_NAME = "your-key-vault-name"

    # Initialize Snowflake integration
    snowflake_integration = AzureSnowflakeIntegration(use_key_vault=USE_KEY_VAULT, key_vault_name=KEY_VAULT_NAME)

    # Example Query
    query = "SELECT CURRENT_DATE;"
    results = snowflake_integration.execute_query(query)

    if results:
        print("\n--- Query Results ---")
        for row in results:
            print(row)
