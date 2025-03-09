"""
Formats and structures AI model responses for user-friendly output in DocuNexus AGI-Agent.
Handles formatting for text responses, data tables, and potentially other output types.
Now optimized for Azure integration and monitoring.
"""

import json
import pandas as pd  # Example for DataFrame formatting
from src.utils.logger import logger  # Import logger
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter  # For Azure Monitoring
from opentelemetry import trace  # OpenTelemetry for tracing

# Initialize Azure Monitor Trace Exporter (for app telemetry)
exporter = AzureMonitorTraceExporter.from_connection_string("<YOUR_AZURE_MONITOR_CONNECTION_STRING>")
tracer = trace.get_tracer(__name__)

class ResponseFormatter:
    def __init__(self):
        logger.info("Azure-enabled ResponseFormatter initialized.")
        with tracer.start_as_current_span("ResponseFormatterInitialization"):
            # Span for telemetry during initialization
            logger.debug("ResponseFormatter telemetry span started.")

    def format_text_response(self, response_text):
        """Formats a raw text response from the AI model."""
        logger.debug("Formatting text response.")
        with tracer.start_as_current_span("FormatTextResponse"):
            formatted_response = response_text.strip()  # Remove leading/trailing whitespace

            # Extract "thoughts" section if present
            thoughts = ""
            parts = formatted_response.split("***DocuNexus Thoughts:***")  # Assuming marker used in prompts
            main_response = parts[0].strip()
            if len(parts) > 1:
                thoughts = parts[1].strip()  # Extract thoughts if available

            tracer.current_span.set_attribute("formatted_response_length", len(main_response))
            tracer.current_span.set_attribute("thoughts_extracted", bool(thoughts))

        return main_response, thoughts

    def format_data_response(self, response_body):
        """
        Formats a response expected to be data (e.g., JSON, list of dictionaries).
        Parses JSON into a Pandas DataFrame if possible, else returns raw response.
        """
        logger.debug("Formatting data response.")
        with tracer.start_as_current_span("FormatDataResponse"):
            try:
                data = json.loads(response_body)  # Attempt to parse JSON
                if isinstance(data, list):  # Convert list of dicts to DataFrame
                    dataframe = pd.DataFrame(data)
                    tracer.current_span.set_attribute("dataframe_rows", len(dataframe))
                    return dataframe
                else:
                    tracer.current_span.set_attribute("is_raw_json", True)
                    return response_body
            except json.JSONDecodeError:
                logger.warning("Response body is not valid JSON. Returning raw response.")
                tracer.current_span.set_attribute("json_decode_error", True)
                return response_body

    def format_error_response(self, error_message):
        """Formats an error message for user display."""
        logger.error(f"Formatting error response: {error_message}")
        with tracer.start_as_current_span("FormatErrorResponse"):
            tracer.current_span.set_attribute("error_message", error_message)
            return f"**Error:** {error_message}. Please check the trace data in the sidebar for details."


# --- Example Usage (outside class definition) ---
if __name__ == "__main__":
    formatter = ResponseFormatter()

    sample_text_response = """
    The key points are:
    1. Data privacy is crucial.
    2. User consent is required.

    ***DocuNexus Thoughts:***
    I identified the key points by looking for numbered lists and keywords like 'crucial' and 'required'.
    """
    formatted, thoughts = formatter.format_text_response(sample_text_response)
    print("\nFormatted Text Response:\n", formatted)
    print("\nExtracted Thoughts:\n", thoughts)

    sample_json_response = """
    [
        {"item": "Item A", "value": 10},
        {"item": "Item B", "value": 25}
    ]
    """
    dataframe_response = formatter.format_data_response(sample_json_response)
    print("\nFormatted Data Response (DataFrame):\n", dataframe_response)

    error_msg = "API connection timed out."
    formatted_error = formatter.format_error_response(error_msg)
    print("\nFormatted Error Response:\n", formatted_error)
