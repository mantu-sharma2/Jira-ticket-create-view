"""
Helper functions for Jira Ticket Manager
Contains utility functions for file operations, data processing, and common operations
"""

import os
import uuid
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_preview_id() -> str:
    """
    Generate a unique preview ID for tracking uploaded data
    
    Returns:
        str: A unique UUID string
    """
    return str(uuid.uuid4())


def generate_operation_id() -> str:
    """
    Generate a unique operation ID for tracking ticket creation processes
    
    Returns:
        str: A unique UUID string
    """
    return str(uuid.uuid4())


def validate_file_extension(filename: str) -> bool:
    """
    Validate if the uploaded file has a valid Excel extension
    
    Args:
        filename (str): Name of the uploaded file
        
    Returns:
        bool: True if file has valid Excel extension, False otherwise
    """
    allowed_extensions = {'.xlsx', '.xls'}
    file_ext = os.path.splitext(filename)[1].lower()
    return file_ext in allowed_extensions


def read_excel_file(file_path: str) -> pd.DataFrame:
    """
    Read Excel file and return DataFrame
    
    Args:
        file_path (str): Path to the Excel file
        
    Returns:
        pd.DataFrame: DataFrame containing the Excel data
        
    Raises:
        Exception: If file cannot be read or is invalid
    """
    try:
        df = pd.read_excel(file_path)
        logger.info(f"Excel file read successfully. Shape: {df.shape}")
        logger.info(f"Columns: {list(df.columns)}")
        return df
    except Exception as e:
        logger.error(f"Error reading Excel file: {e}")
        raise Exception(f"Failed to read Excel file: {str(e)}")


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and prepare DataFrame for processing
    
    Args:
        df (pd.DataFrame): Raw DataFrame from Excel
        
    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    # Remove completely empty rows
    df = df.dropna(how='all')
    
    # Remove completely empty columns
    df = df.dropna(axis=1, how='all')
    
    # Fill NaN values with empty strings
    df = df.fillna('')
    
    # Strip whitespace from string columns
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].astype(str).str.strip()
    
    return df


def convert_dataframe_to_dict(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Convert DataFrame to list of dictionaries for JSON serialization
    
    Args:
        df (pd.DataFrame): DataFrame to convert
        
    Returns:
        List[Dict[str, Any]]: List of dictionaries representing rows
    """
    return df.to_dict('records')


def format_timestamp() -> str:
    """
    Get current timestamp in a readable format
    
    Returns:
        str: Formatted timestamp string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_error_response(message: str, status_code: int = 400) -> Dict[str, Any]:
    """
    Create a standardized error response
    
    Args:
        message (str): Error message
        status_code (int): HTTP status code
        
    Returns:
        Dict[str, Any]: Standardized error response
    """
    return {
        "success": False,
        "error": message,
        "status_code": status_code,
        "timestamp": format_timestamp()
    }


def create_success_response(data: Any = None, message: str = "Success") -> Dict[str, Any]:
    """
    Create a standardized success response
    
    Args:
        data (Any): Response data
        message (str): Success message
        
    Returns:
        Dict[str, Any]: Standardized success response
    """
    response = {
        "success": True,
        "message": message,
        "timestamp": format_timestamp()
    }
    
    if data is not None:
        response["data"] = data
        
    return response


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent security issues
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Remove path traversal characters
    filename = os.path.basename(filename)
    
    # Remove or replace dangerous characters
    dangerous_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
    for char in dangerous_chars:
        filename = filename.replace(char, '_')
    
    return filename


def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in megabytes
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        float: File size in MB
    """
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    except OSError:
        return 0.0


def ensure_directory_exists(directory_path: str) -> None:
    """
    Ensure a directory exists, create if it doesn't
    
    Args:
        directory_path (str): Path to the directory
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        logger.info(f"Created directory: {directory_path}")


def cleanup_old_files(directory: str, max_age_hours: int = 24) -> None:
    """
    Clean up old files in a directory
    
    Args:
        directory (str): Directory to clean
        max_age_hours (int): Maximum age of files in hours
    """
    try:
        current_time = datetime.now()
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                age_hours = (current_time - file_time).total_seconds() / 3600
                
                if age_hours > max_age_hours:
                    os.remove(file_path)
                    logger.info(f"Cleaned up old file: {filename}")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}") 