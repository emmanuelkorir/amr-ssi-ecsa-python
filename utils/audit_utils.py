# utils/audit_utils.py
import pandas as pd
import os
import logging
from datetime import datetime

# Get the logger instance
logger = logging.getLogger("amr_ssi_pipeline")

def log_exclusion(study_id, reason, file_path="logs/missing_data_log.csv"):
    """
    Logs a study or data row exclusion to a structured CSV file.

    This function appends a record to the specified log file, creating the file
    and writing the header if it doesn't exist. This creates a fully auditable
    trail of all data points excluded from any analysis.

    Args:
        study_id (str or int): The unique identifier for the study or row being excluded.
        reason (str): A clear, specific reason for the exclusion.
        file_path (str, optional): The path to the exclusion log file. 
                                   Defaults to "logs/missing_data_log.csv".
    """
    try:
        # Ensure the directory for the log file exists
        log_dir = os.path.dirname(file_path)
        os.makedirs(log_dir, exist_ok=True)

        # Define the data to be appended
        new_entry = pd.DataFrame({
            'timestamp': [datetime.now()],
            'study_id': [study_id],
            'reason_for_exclusion': [reason]
        })

        # If the file doesn't exist, create it and write the header
        if not os.path.exists(file_path):
            logger.info(f"Creating new exclusion log file at: {file_path}")
            new_entry.to_csv(file_path, index=False)
        else:
            # Append without writing the header
            new_entry.to_csv(file_path, mode='a', header=False, index=False)
        
        logger.debug(f"Logged exclusion for study '{study_id}' due to: {reason}")

    except Exception as e:
        logger.error(f"Failed to log exclusion for study '{study_id}'. Error: {e}", exc_info=True)

