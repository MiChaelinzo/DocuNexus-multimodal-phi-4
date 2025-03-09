from src.utils.logger import logger  # Import logger
from azure.ai.openai import OpenAIClient
from azure.core.credentials import AzureKeyCredential

class AzurePromptTemplates:
    def __init__(self, azure_api_key, azure_endpoint, model_name="gpt-4"):
        """
        Initialize the PromptTemplates class with Azure OpenAI client.

        Args:
            azure_api_key (str): Azure OpenAI API Key.
            azure_endpoint (str): Azure OpenAI Endpoint.
            model_name (str): Azure OpenAI model to use (default is 'gpt-4').
        """
        logger.info("AzurePromptTemplates initialized.")
        self.client = OpenAIClient(endpoint=azure_endpoint, credential=AzureKeyCredential(azure_api_key))
        self.model_name = model_name

    def create_prompt(self, task_type, user_prompt, context=None, **kwargs):
        """
        Creates a prompt based on the task type and user input, potentially adding context.

        Args:
            task_type (str): Type of task (e.g., "document_analysis", "media_summarization").
            user_prompt (str): User's request or question.
            context (str, list, optional): Contextual information (e.g., document text, list of documents). Defaults to None.
            **kwargs: Additional keyword arguments for template customization.

        Returns:
            str: The formatted prompt string ready to be sent to the AI model.
        """
        logger.debug(f"Creating Azure-enabled prompt for task type: {task_type}")

        if task_type == "document_analysis":
            return self._document_analysis_prompt(user_prompt, context, **kwargs)
        elif task_type == "media_summarization":
            return self._media_summarization_prompt(user_prompt, context, **kwargs)
        elif task_type == "webcam_vision_analysis":
            return self._webcam_vision_prompt(user_prompt, **kwargs)
        else:
            logger.warning(f"No specific template found for task type: {task_type}. Using default.")
            return self._default_prompt(user_prompt, context)

    def _document_analysis_prompt(self, user_prompt, context_documents, response_length="comprehensive", language="English", request_thoughts=True, **kwargs):
        """Template for document analysis tasks."""
        prompt = f"""
        [Azure DocuNexus AGI - Document Analysis Task]

        You are Azure DocuNexus, an intelligent AGI agent powered by Azure OpenAI, specializing in document analysis. 
        Your goal is to deeply analyze the provided documents and respond to the user's request with a {response_length} response in {language}.

        **User Request:**
        {user_prompt}

        **Context Documents:**
        ---Document Start---
        {chr(10).join(context_documents) if context_documents else 'No documents provided.'}
        ---Document End---

        Response Guidelines:
        * Provide a clear, comprehensive, and detailed answer that directly addresses the user's request.
        * Use bullet points or numbered lists where appropriate for clarity.
        * Focus on extracting key insights and actionable information from the documents.
        """
        if request_thoughts:
            prompt += "\n***DocuNexus Azure Thoughts:*** Include a section at the end, marked '***DocuNexus Azure Thoughts:***', explaining your reasoning step-by-step."
        return prompt

    def _media_summarization_prompt(self, user_prompt, media_description, response_length="concise", language="English", request_thoughts=False, **kwargs):
        """Template for media summarization tasks."""
        prompt = f"""
        [Azure DocuNexus AGI - Media Summarization Task]

        You are Azure DocuNexus, an intelligent AGI agent powered by Azure OpenAI, specializing in media summarization. 
        Your goal is to summarize the media content based on the user's request in a {response_length} response in {language}.

        **User Request:**
        {user_prompt}

        **Media Description:**
        {media_description or 'No media description provided.'}

        Response Guidelines:
        * Provide a concise and informative summary of the media content relevant to the user's query.
        * Focus on key themes, objects, or information present in the media.
        """
        if request_thoughts:
            prompt += "\n***DocuNexus Azure Thoughts:*** Include a brief section marked '***DocuNexus Azure Thoughts:***' explaining your reasoning."
        return prompt

    def _webcam_vision_prompt(self, user_prompt, response_length="detailed", language="English", request_thoughts=True, **kwargs):
        """Template for webcam vision analysis tasks."""
        prompt = f"""
        [Azure DocuNexus AGI - Webcam Vision Analysis Task]

        You are Azure DocuNexus, an intelligent AGI agent powered by Azure OpenAI, specializing in real-time webcam analysis. 
        Your goal is to analyze the live webcam feed and answer the user's question in a {response_length} response in {language}.

        **User Question:**
        {user_prompt}

        **Instructions:**
        * Analyze objects, scenes, and activities visible in the webcam feed.
        * Provide detailed insights, interpretations, and relevant information based on your analysis.
        """
        if request_thoughts:
            prompt += "\n***DocuNexus Azure Thoughts:*** Include a section at the end, marked '***DocuNexus Azure Thoughts:***', explaining your step-by-step analysis process."
        return prompt

    def _default_prompt(self, user_prompt, context=None):
        """Default fallback prompt."""
        return f"""
        [Azure DocuNexus AGI - General Inquiry]

        **User Question:**
        {user_prompt}

        **Context:**
        {context or 'None'}

        **Response Guidelines:**
        Provide a clear and helpful answer that directly addresses the user's question, incorporating any context provided.
        """

# Example usage:
# azure_templates = AzurePromptTemplates(azure_api_key="YOUR_API_KEY", azure_endpoint="YOUR_ENDPOINT")
# prompt = azure_templates.create_prompt(task_type="document_analysis", user_prompt="Analyze this document.", context=["Example text"])
