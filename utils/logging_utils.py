# utils/logging_utils.py
import logging
import sys
from datetime import datetime
import os

def setup_logging(log_dir="logs", file_prefix="pipeline"):
    """
    Sets up a centralized logger for the project.

    This function creates a logger that outputs to both the console (INFO level)
    and a timestamped file (DEBUG level) in the specified log directory.
    It ensures the log directory exists.

    Args:
        log_dir (str): The directory to save log files in. Defaults to "logs".
        file_prefix (str): A prefix for the log file name. Defaults to "pipeline".

    Returns:
        logging.Logger: The configured logger instance.
    """
    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Create a logger
    logger = logging.getLogger("amr_ssi_pipeline")
    logger.setLevel(logging.DEBUG)  # Set the lowest level to capture all messages

    # Prevent duplicate handlers if called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    # --- File Handler ---
    # Create a timestamped log file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"{file_prefix}_{timestamp}.log")

    # Create file handler which logs even debug messages
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(module)s.%(funcName)s - %(message)s"
    )
    fh.setFormatter(file_formatter)
    logger.addHandler(fh)

    # --- Console Handler ---
    # Create console handler with a higher log level
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)  # Only show INFO and above on the console
    console_formatter = logging.Formatter("%(levelname)s: %(message)s")
    ch.setFormatter(console_formatter)
    logger.addHandler(ch)

    logger.info(f"Logging initialized. Log file: {log_file}")

    return logger
