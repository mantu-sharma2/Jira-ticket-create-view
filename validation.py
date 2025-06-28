"""
Validation functions for Jira Ticket Manager
Contains data validation logic for Excel files and ticket creation
"""

import logging
from typing import Dict, List, Any, Tuple, Optional
import pandas as pd
from helpers import validate_file_extension

# Configure logging
logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


def validate_excel_structure(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate that the Excel file has the required structure and columns
    
    Args:
        df (pd.DataFrame): DataFrame to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    try:
        # Check if DataFrame is empty
        if df.empty:
            return False, "Excel file is empty"
        
        # Check minimum required columns
        required_columns = {'summary', 'description', 'issue_type', 'priority'}
        available_columns = set(df.columns)
        
        missing_columns = required_columns - available_columns
        if missing_columns:
            return False, f"Missing required columns: {', '.join(missing_columns)}"
        
        # Check if there are any rows with data
        if len(df) == 0:
            return False, "No data rows found in Excel file"
        
        return True, "Data validation passed"
        
    except Exception as e:
        logger.error(f"Validation error: {e}")
        return False, f"Validation error: {str(e)}"


def validate_ticket_data(row: Dict[str, Any], row_index: int) -> Tuple[bool, str]:
    """
    Validate individual ticket data row
    
    Args:
        row (Dict[str, Any]): Row data as dictionary
        row_index (int): Index of the row for error reporting
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    try:
        # Validate required fields are not empty
        required_fields = ['summary', 'description', 'issue_type', 'priority']
        
        for field in required_fields:
            if not row.get(field) or str(row.get(field)).strip() == '':
                return False, f"Row {row_index + 1}: {field} is required and cannot be empty"
        
        # Validate issue_type
        valid_issue_types = {'bug', 'task', 'story', 'epic', 'subtask'}
        issue_type = str(row.get('issue_type', '')).lower().strip()
        if issue_type not in valid_issue_types:
            return False, f"Row {row_index + 1}: Invalid issue_type '{row.get('issue_type')}'. Must be one of: {', '.join(valid_issue_types)}"
        
        # Validate priority
        valid_priorities = {'low', 'medium', 'high', 'critical', 'highest'}
        priority = str(row.get('priority', '')).lower().strip()
        if priority not in valid_priorities:
            return False, f"Row {row_index + 1}: Invalid priority '{row.get('priority')}'. Must be one of: {', '.join(valid_priorities)}"
        
        # Validate summary length
        summary = str(row.get('summary', '')).strip()
        if len(summary) > 255:
            return False, f"Row {row_index + 1}: Summary is too long (max 255 characters)"
        
        # Validate description length
        description = str(row.get('description', '')).strip()
        if len(description) > 32767:
            return False, f"Row {row_index + 1}: Description is too long (max 32767 characters)"
        
        return True, "Row validation passed"
        
    except Exception as e:
        logger.error(f"Row validation error at row {row_index + 1}: {e}")
        return False, f"Row {row_index + 1}: Validation error - {str(e)}"


def validate_all_tickets(df: pd.DataFrame) -> Tuple[bool, str, List[int]]:
    """
    Validate all ticket rows in the DataFrame
    
    Args:
        df (pd.DataFrame): DataFrame containing ticket data
        
    Returns:
        Tuple[bool, str, List[int]]: (is_valid, error_message, invalid_row_indices)
    """
    invalid_rows = []
    
    for index, row in df.iterrows():
        row_dict = row.to_dict()
        is_valid, error_message = validate_ticket_data(row_dict, index)
        
        if not is_valid:
            invalid_rows.append(index)
            logger.warning(f"Invalid row {index + 1}: {error_message}")
    
    if invalid_rows:
        return False, f"Validation failed for {len(invalid_rows)} rows", invalid_rows
    
    return True, "All tickets validated successfully", []


def validate_file_size(file_size_mb: float, max_size_mb: float = 10.0) -> Tuple[bool, str]:
    """
    Validate file size is within acceptable limits
    
    Args:
        file_size_mb (float): File size in megabytes
        max_size_mb (float): Maximum allowed file size in megabytes
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if file_size_mb > max_size_mb:
        return False, f"File size ({file_size_mb:.2f}MB) exceeds maximum allowed size ({max_size_mb}MB)"
    
    if file_size_mb <= 0:
        return False, "File size is invalid or file is empty"
    
    return True, "File size validation passed"


def validate_filename(filename: str) -> Tuple[bool, str]:
    """
    Validate filename for security and format
    
    Args:
        filename (str): Name of the file to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not filename:
        return False, "Filename is empty"
    
    if not validate_file_extension(filename):
        return False, "Invalid file extension. Only .xlsx and .xls files are allowed"
    
    # Check for dangerous characters
    dangerous_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
    for char in dangerous_chars:
        if char in filename:
            return False, f"Filename contains invalid character: {char}"
    
    # Check filename length
    if len(filename) > 255:
        return False, "Filename is too long (max 255 characters)"
    
    return True, "Filename validation passed"


def validate_project_key(project_key: str) -> Tuple[bool, str]:
    """
    Validate Jira project key format
    
    Args:
        project_key (str): Project key to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not project_key:
        return True, "Project key is optional"
    
    project_key = str(project_key).strip()
    
    # Jira project keys are typically 2-10 characters, uppercase letters and numbers
    if len(project_key) < 2 or len(project_key) > 10:
        return False, "Project key must be between 2 and 10 characters"
    
    if not project_key.isalnum():
        return False, "Project key must contain only letters and numbers"
    
    return True, "Project key validation passed"


def validate_assignee(assignee: str) -> Tuple[bool, str]:
    """
    Validate assignee field
    
    Args:
        assignee (str): Assignee to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not assignee:
        return True, "Assignee is optional"
    
    assignee = str(assignee).strip()
    
    # Check length
    if len(assignee) > 100:
        return False, "Assignee name is too long (max 100 characters)"
    
    # Check for valid characters (letters, numbers, spaces, dots, hyphens, underscores)
    import re
    if not re.match(r'^[a-zA-Z0-9\s\.\-_]+$', assignee):
        return False, "Assignee name contains invalid characters"
    
    return True, "Assignee validation passed"


def validate_labels(labels: str) -> Tuple[bool, str]:
    """
    Validate labels field
    
    Args:
        labels (str): Labels to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not labels:
        return True, "Labels are optional"
    
    labels = str(labels).strip()
    
    # Check length
    if len(labels) > 1000:
        return False, "Labels are too long (max 1000 characters)"
    
    # Split by comma and validate individual labels
    label_list = [label.strip() for label in labels.split(',') if label.strip()]
    
    for label in label_list:
        if len(label) > 50:
            return False, f"Label '{label}' is too long (max 50 characters)"
        
        # Check for valid characters
        import re
        if not re.match(r'^[a-zA-Z0-9\-_]+$', label):
            return False, f"Label '{label}' contains invalid characters"
    
    return True, "Labels validation passed"


def comprehensive_validation(df: pd.DataFrame, file_size_mb: float = 0.0) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Perform comprehensive validation of the entire Excel file
    
    Args:
        df (pd.DataFrame): DataFrame to validate
        file_size_mb (float): File size in megabytes
        
    Returns:
        Tuple[bool, str, Dict[str, Any]]: (is_valid, error_message, validation_details)
    """
    validation_details = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'invalid_rows': [],
        'warnings': []
    }
    
    # Validate file structure
    is_valid, error_message = validate_excel_structure(df)
    if not is_valid:
        return False, error_message, validation_details
    
    # Validate file size
    if file_size_mb > 0:
        is_valid, error_message = validate_file_size(file_size_mb)
        if not is_valid:
            validation_details['warnings'].append(error_message)
    
    # Validate all ticket rows
    is_valid, error_message, invalid_rows = validate_all_tickets(df)
    validation_details['invalid_rows'] = invalid_rows
    
    if not is_valid:
        return False, error_message, validation_details
    
    # Additional validations for optional fields
    for index, row in df.iterrows():
        row_dict = row.to_dict()
        
        # Validate project key
        if 'project_key' in row_dict:
            is_valid, error_message = validate_project_key(row_dict['project_key'])
            if not is_valid:
                validation_details['warnings'].append(f"Row {index + 1}: {error_message}")
        
        # Validate assignee
        if 'assignee' in row_dict:
            is_valid, error_message = validate_assignee(row_dict['assignee'])
            if not is_valid:
                validation_details['warnings'].append(f"Row {index + 1}: {error_message}")
        
        # Validate labels
        if 'labels' in row_dict:
            is_valid, error_message = validate_labels(row_dict['labels'])
            if not is_valid:
                validation_details['warnings'].append(f"Row {index + 1}: {error_message}")
    
    success_message = f"Validation passed for {len(df)} tickets"
    if validation_details['warnings']:
        success_message += f" with {len(validation_details['warnings'])} warnings"
    
    return True, success_message, validation_details 