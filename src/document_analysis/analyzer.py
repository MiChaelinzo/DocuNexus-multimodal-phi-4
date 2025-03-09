"""
Azure-enabled module for deep document analysis within DocuNexus AGI-Agent.
Supports comparative analysis, entity extraction, and semantic reasoning.
"""

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.openai import OpenAIClient
from azure.core.exceptions import AzureError
from src.utils.logger import logger  # Import logger


class AzureDocumentAnalyzer:
    def __init__(self, form_recognizer_endpoint, form_recognizer_key, openai_endpoint, openai_api_key, model_name="gpt-4"):
        """
        Initializes the AzureDocumentAnalyzer with Azure Cognitive Services.

        Args:
            form_recognizer_endpoint (str): Azure Form Recognizer endpoint.
            form_recognizer_key (str): Azure Form Recognizer API key.
            openai_endpoint (str): Azure OpenAI endpoint.
            openai_api_key (str): Azure OpenAI API key.
            model_name (str): Model name for Azure OpenAI (default: "gpt-4").
        """
        self.form_recognizer_client = DocumentAnalysisClient(
            endpoint=form_recognizer_endpoint,
            credential=AzureKeyCredential(form_recognizer_key)
        )
        self.openai_client = OpenAIClient(
            endpoint=openai_endpoint,
            credential=AzureKeyCredential(openai_api_key)
        )
        self.model_name = model_name
        logger.info("AzureDocumentAnalyzer initialized with Form Recognizer and OpenAI.")

    def extract_entities(self, document):
        """
        Extracts entities from the document using Azure Form Recognizer.

        Args:
            document (bytes): The document content in bytes (PDF, image).

        Returns:
            dict: Extracted entities and key-value pairs.
        """
        logger.debug("Extracting entities using Azure Form Recognizer.")

        try:
            poller = self.form_recognizer_client.begin_analyze_document(
                model_id="prebuilt-document",
                document=document
            )
            result = poller.result()

            entities = {}
            for kv_pair in result.key_value_pairs:
                key = kv_pair.key.content if kv_pair.key else "N/A"
                value = kv_pair.value.content if kv_pair.value else "N/A"
                entities[key] = value

            logger.info("Entity extraction completed successfully.")
            return entities

        except AzureError as e:
            logger.error(f"Error extracting entities: {e}")
            return {"error": str(e)}

    def compare_documents(self, document_texts, comparison_prompt="Compare these documents for similarities and differences."):
        """
        Compares multiple documents using Azure OpenAI for deeper reasoning.

        Args:
            document_texts (list): A list of document texts to compare.
            comparison_prompt (str): Prompt to guide the AI in comparing the documents.

        Returns:
            str: AI-generated comparison summary.
        """
        logger.debug("Starting document comparison using Azure OpenAI.")

        try:
            # Constructing the prompt
            formatted_prompt = comparison_prompt + "\n\n" + "\n\n---\n\n".join(document_texts)

            response = self.openai_client.get_chat_completions(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are an expert in document comparison and analysis."},
                    {"role": "user", "content": formatted_prompt}
                ],
                max_tokens=2000  # Adjust based on expected response size
            )

            comparison_summary = response.choices[0].message["content"]
            logger.info("Document comparison completed successfully.")
            return comparison_summary

        except AzureError as e:
            logger.error(f"Error during document comparison: {e}")
            return f"Error occurred: {e}"

    def semantic_search(self, document_text, query):
        """
        Performs semantic search within a document using Azure OpenAI.

        Args:
            document_text (str): The text content of the document.
            query (str): The search query.

        Returns:
            str: AI-generated search results.
        """
        logger.debug("Starting semantic search using Azure OpenAI.")

        try:
            # Constructing the prompt
            prompt = f"Search the following document for information related to: {query}\n\nDocument:\n{document_text}"

            response = self.openai_client.get_chat_completions(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are an expert in semantic search within documents."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500  # Adjust token limit based on response complexity
            )

            search_results = response.choices[0].message["content"]
            logger.info("Semantic search completed successfully.")
            return search_results

        except AzureError as e:
            logger.error(f"Error during semantic search: {e}")
            return f"Error occurred: {e}"


# --- Example Usage ---
if __name__ == "__main__":
    # Replace with your Azure credentials
    FORM_RECOGNIZER_ENDPOINT = "YOUR_FORM_RECOGNIZER_ENDPOINT"
    FORM_RECOGNIZER_KEY = "YOUR_FORM_RECOGNIZER_KEY"
    OPENAI_ENDPOINT = "YOUR_OPENAI_ENDPOINT"
    OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

    analyzer = AzureDocumentAnalyzer(
        form_recognizer_endpoint=FORM_RECOGNIZER_ENDPOINT,
        form_recognizer_key=FORM_RECOGNIZER_KEY,
        openai_endpoint=OPENAI_ENDPOINT,
        openai_api_key=OPENAI_API_KEY
    )

    # Example usage for entity extraction
    with open("sample.pdf", "rb") as f:
        extracted_entities = analyzer.extract_entities(f.read())
        print("\n--- Extracted Entities ---")
        print(extracted_entities)

    # Example usage for document comparison
    doc1 = "Document 1 text content..."
    doc2 = "Document 2 text content..."
    comparison = analyzer.compare_documents([doc1, doc2])
    print("\n--- Document Comparison ---")
    print(comparison)

    # Example usage for semantic search
    document_text = "Complete text of the document here..."
    query = "Find all clauses about data privacy."
    search_results = analyzer.semantic_search(document_text, query)
    print("\n--- Semantic Search Results ---")
    print(search_results)
