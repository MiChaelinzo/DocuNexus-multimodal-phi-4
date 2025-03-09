"""
Azure-enabled module for document summarization tasks within DocuNexus AGI-Agent.
This module integrates with Azure OpenAI services to handle summarization and reasoning tasks.
"""

from azure.ai.openai import OpenAIClient
from azure.core.credentials import AzureKeyCredential
from src.utils.logger import logger  # Import logger


class AzureDocumentSummarizer:
    def __init__(self, azure_api_key, azure_endpoint, model_name="gpt-4"):
        """
        Initializes the AzureDocumentSummarizer with Azure OpenAI client.

        Args:
            azure_api_key (str): Azure OpenAI API Key.
            azure_endpoint (str): Azure OpenAI Endpoint.
            model_name (str): Model name to be used for summarization (e.g., "gpt-4").
        """
        self.client = OpenAIClient(endpoint=azure_endpoint, credential=AzureKeyCredential(azure_api_key))
        self.model_name = model_name
        logger.info("AzureDocumentSummarizer initialized with Azure OpenAI.")

    def summarize_document(self, document_text, summary_length="concise", request_thoughts=True):
        """
        Summarizes document text using Azure OpenAI.

        Args:
            document_text (str): Text content of the document to summarize.
            summary_length (str): Desired summary length ("concise", "detailed", "comprehensive").
            request_thoughts (bool): Whether to request reasoning/thought process for the summary.

        Returns:
            tuple: (summary_text, thoughts_text) - Summary and reasoning (if requested).
        """
        logger.debug(f"Starting document summarization with length: {summary_length}")

        # Constructing the system and user prompt
        prompt = f"Summarize the following document in a {summary_length} manner:\n\n{document_text}"
        if request_thoughts:
            prompt += "\nPlease also provide your reasoning and thought process behind this summary."

        try:
            response = self.client.get_chat_completions(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are an AI summarization expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000  # Adjust based on expected response size
            )

            # Extracting the AI's response
            summary_text = response.choices[0].message["content"]
            logger.info(f"Summarization completed successfully. Summary Length: {len(summary_text)}")

            # Attempt to parse thoughts if they are explicitly requested
            thoughts_text = ""
            if request_thoughts:
                parts = summary_text.split("***Thought Process:***")
                main_summary = parts[0].strip()
                if len(parts) > 1:
                    thoughts_text = parts[1].strip()
                else:
                    thoughts_text = "Thought process section was not explicitly provided."

                return main_summary, thoughts_text

            return summary_text, None
        except Exception as e:
            logger.error(f"Error during document summarization: {e}")
            return f"Error occurred: {e}", None


# --- Example Usage ---
if __name__ == "__main__":
    # Replace with your Azure OpenAI credentials
    AZURE_API_KEY = "YOUR_AZURE_API_KEY"
    AZURE_ENDPOINT = "YOUR_AZURE_ENDPOINT"

    summarizer = AzureDocumentSummarizer(azure_api_key=AZURE_API_KEY, azure_endpoint=AZURE_ENDPOINT)

    sample_document_text = (
        "This is a sample document. It discusses several topics, including point A, point B, and point C. "
        "Point A is very important because... Point B is also significant because... Finally, point C is "
        "relevant due to..."
    )

    summary, thoughts = summarizer.summarize_document(
        sample_document_text, summary_length="concise", request_thoughts=True
    )

    print("\n--- Document Summary ---")
    print(summary)
    if thoughts:
        print("\n--- Azure AI Thought Process ---")
        print(thoughts)
