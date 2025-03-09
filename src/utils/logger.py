"""
Azure-enabled logging setup for DocuNexus AGI-Agent.
Configures logging to console and Azure Monitor for application events and errors.
For production, integrates with Azure Monitor using OpenTelemetry for robust logging solutions.
"""

import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.azure.monitor import AzureMonitorTraceExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

# Configure OpenTelemetry for Azure Monitor
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "DocuNexus AGI-Agent"})
    )
)
exporter = AzureMonitorTraceExporter.from_connection_string(
    "YOUR_AZURE_MONITOR_CONNECTION_STRING"
)  # Replace with your Azure Monitor connection string
span_processor = BatchSpanProcessor(exporter)
trace.get_tracer_provider().add_span_processor(span_processor)
tracer = trace.get_tracer(__name__)

# Configure basic logging to console
logging.basicConfig(
    level=logging.INFO,  # Default log level - can be adjusted via config or env vars
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("DocuNexusLogger")  # Get logger instance for this module


def log_to_azure(message, level="INFO"):
    """
    Logs messages to Azure Monitor using OpenTelemetry.
    Args:
        message (str): The log message.
        level (str): Log level ('INFO', 'WARNING', 'ERROR', 'DEBUG').
    """
    with tracer.start_as_current_span("AzureMonitorLog"):
        if level == "INFO":
            logger.info(message)
        elif level == "WARNING":
            logger.warning(message)
        elif level == "ERROR":
            logger.error(message)
        elif level == "DEBUG":
            logger.debug(message)
        else:
            logger.error(f"Unsupported log level: {level}")


# --- Example Usage ---
if __name__ == "__main__":
    logger.info("This is an info message from the logger.")
    logger.debug("This is a debug message (not shown by default).")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")

    # Example of logging to Azure Monitor
    log_to_azure("This is a test log sent to Azure Monitor.", level="INFO")
    log_to_azure("This is a warning log sent to Azure Monitor.", level="WARNING")
    log_to_azure("This is an error log sent to Azure Monitor.", level="ERROR")
