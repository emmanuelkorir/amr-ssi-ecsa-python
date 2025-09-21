# utils/data_loader.py
import pandas as pd
import os
import logging

# Get the logger instance from the logging utility
logger = logging.getLogger("amr_ssi_pipeline")

def load_data(file_path):
    """
    Loads a single CSV or Excel file into a pandas DataFrame with robust error handling.

    Args:
        file_path (str): The full path to the data file.

    Returns:
        pd.DataFrame or None: The loaded DataFrame, or None if the file cannot be loaded.
    """
    if not os.path.exists(file_path):
        logger.warning(f"File not found: {file_path}. Skipping.")
        return None

    try:
        logger.info(f"Attempting to load data from: {file_path}")
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path)
        else:
            logger.warning(f"Unsupported file type for: {file_path}. Only .csv and .xlsx are supported. Skipping.")
            return None
        
        logger.info(f"Successfully loaded {len(df)} rows from {os.path.basename(file_path)}.")
        return df

    except Exception as e:
        logger.error(f"Failed to load or process file {file_path}. Error: {e}", exc_info=True)
        return None

def load_all_data(data_dir):
    """
    Loads all supported data files from a specified directory.

    Args:
        data_dir (str): The path to the directory containing data files.

    Returns:
        dict: A dictionary where keys are filenames and values are the loaded DataFrames.
              Files that fail to load will not be included in the dictionary.
    """
    all_data = {}
    if not os.path.isdir(data_dir):
        logger.warning(f"Data directory not found: {data_dir}. Cannot load any data.")
        return all_data

    for filename in os.listdir(data_dir):
        file_path = os.path.join(data_dir, filename)
        if os.path.isfile(file_path) and (filename.endswith('.csv') or filename.endswith('.xlsx')):
            df = load_data(file_path)
            if df is not None:
                # Use the filename without extension as the key
                clean_filename = os.path.splitext(filename)[0]
                all_data[clean_filename] = df
    
    if not all_data:
        logger.warning(f"No data files were successfully loaded from {data_dir}.")
    
    return all_data
