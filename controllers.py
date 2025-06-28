"""
Controllers for Jira Ticket Manager
Handles business logic and coordinates between different services
"""

import logging
import os
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import threading
import time

from helpers import (
    generate_preview_id, generate_operation_id, read_excel_file, clean_dataframe,
    convert_dataframe_to_dict, get_file_size_mb, sanitize_filename, ensure_directory_exists,
    create_error_response, create_success_response
)
from validation import comprehensive_validation, validate_filename
from jira_service import get_jira_service, validate_jira_config

# Configure logging
logger = logging.getLogger(__name__)

# Global storage for preview data and operations
preview_data_store = {}
operation_status_store = {}


class FileUploadController:
    """
    Controller for handling file upload operations
    """
    
    def __init__(self):
        """Initialize the file upload controller"""
        self.upload_dir = "uploads"
        ensure_directory_exists(self.upload_dir)
    
    def process_file_upload(self, file) -> Dict[str, Any]:
        """
        Process uploaded Excel file and validate data
        
        Args:
            file: Uploaded file object from Flask
            
        Returns:
            Dict[str, Any]: Processing result with preview data or error
        """
        try:
            # Validate filename
            filename = sanitize_filename(file.filename)
            is_valid, error_message = validate_filename(filename)
            if not is_valid:
                return create_error_response(error_message)
            
            # Save file temporarily
            file_path = os.path.join(self.upload_dir, filename)
            file.save(file_path)
            
            # Get file size
            file_size_mb = get_file_size_mb(file_path)
            
            # Read and process Excel file
            df = read_excel_file(file_path)
            df = clean_dataframe(df)
            
            # Validate data
            is_valid, validation_message, validation_details = comprehensive_validation(df, file_size_mb)
            
            if not is_valid:
                # Clean up file
                os.remove(file_path)
                return create_error_response(validation_message)
            
            # Generate preview ID and store data
            preview_id = generate_preview_id()
            preview_data = {
                'file_path': file_path,
                'filename': filename,
                'data': convert_dataframe_to_dict(df),
                'columns': list(df.columns),
                'total_rows': len(df),
                'validation_details': validation_details,
                'created_at': datetime.now().isoformat()
            }
            
            preview_data_store[preview_id] = preview_data
            
            # Clean up old preview data (older than 1 hour)
            self._cleanup_old_previews()
            
            logger.info(f"File upload successful: {filename} -> {preview_id}")
            
            return create_success_response({
                'preview_id': preview_id,
                'columns': list(df.columns),
                'data': preview_data['data'],
                'total_rows': len(df),
                'validation_message': validation_message
            })
            
        except Exception as e:
            logger.error(f"File upload error: {e}")
            return create_error_response(f"File processing failed: {str(e)}")
    
    def get_preview_data(self, preview_id: str) -> Optional[Dict[str, Any]]:
        """
        Get preview data by ID
        
        Args:
            preview_id (str): Preview ID
            
        Returns:
            Optional[Dict[str, Any]]: Preview data or None if not found
        """
        return preview_data_store.get(preview_id)
    
    def _cleanup_old_previews(self, max_age_hours: int = 1):
        """
        Clean up old preview data
        
        Args:
            max_age_hours (int): Maximum age in hours
        """
        current_time = datetime.now()
        to_remove = []
        
        for preview_id, data in preview_data_store.items():
            created_at = datetime.fromisoformat(data['created_at'])
            age_hours = (current_time - created_at).total_seconds() / 3600
            
            if age_hours > max_age_hours:
                to_remove.append(preview_id)
                # Clean up file
                try:
                    if os.path.exists(data['file_path']):
                        os.remove(data['file_path'])
                except Exception as e:
                    logger.error(f"Error cleaning up file {data['file_path']}: {e}")
        
        for preview_id in to_remove:
            del preview_data_store[preview_id]
            logger.info(f"Cleaned up old preview: {preview_id}")


class TicketCreationController:
    """
    Controller for handling ticket creation operations
    """
    
    def __init__(self):
        """Initialize the ticket creation controller"""
        self.file_controller = FileUploadController()
    
    def start_ticket_creation(self, preview_id: str) -> Dict[str, Any]:
        """
        Start ticket creation process for a preview
        
        Args:
            preview_id (str): Preview ID to create tickets for
            
        Returns:
            Dict[str, Any]: Operation result with operation ID or error
        """
        try:
            # Get preview data
            preview_data = self.file_controller.get_preview_data(preview_id)
            if not preview_data:
                return create_error_response("Preview data not found or expired")
            
            # Validate Jira configuration
            is_valid, error_message = validate_jira_config()
            if not is_valid:
                return create_error_response(f"Jira configuration error: {error_message}")
            
            # Generate operation ID
            operation_id = generate_operation_id()
            
            # Initialize operation status
            operation_status = {
                'operation_id': operation_id,
                'preview_id': preview_id,
                'status': 'processing',
                'total_tickets': len(preview_data['data']),
                'completed': 0,
                'failed': 0,
                'tickets': [],
                'errors': [],
                'started_at': datetime.now().isoformat(),
                'completed_at': None
            }
            
            operation_status_store[operation_id] = operation_status
            
            # Start ticket creation in background thread
            thread = threading.Thread(
                target=self._create_tickets_background,
                args=(operation_id, preview_data['data'])
            )
            thread.daemon = True
            thread.start()
            
            logger.info(f"Started ticket creation: {operation_id} for {len(preview_data['data'])} tickets")
            
            return create_success_response({
                'operation_id': operation_id,
                'total_tickets': len(preview_data['data'])
            })
            
        except Exception as e:
            logger.error(f"Ticket creation start error: {e}")
            return create_error_response(f"Failed to start ticket creation: {str(e)}")
    
    def _create_tickets_background(self, operation_id: str, tickets_data: List[Dict[str, Any]]):
        """
        Create tickets in background thread
        
        Args:
            operation_id (str): Operation ID
            tickets_data (List[Dict[str, Any]]): List of ticket data
        """
        try:
            # Get Jira service
            jira_service = get_jira_service()
            if not jira_service:
                self._update_operation_status(operation_id, 'failed', error="Jira service not available")
                return
            
            # Create tickets
            results = jira_service.create_multiple_tickets(tickets_data)
            
            # Update operation status
            operation_status = operation_status_store.get(operation_id)
            if operation_status:
                operation_status['status'] = 'completed'
                operation_status['completed'] = results['successful']
                operation_status['failed'] = results['failed']
                operation_status['tickets'] = results['tickets']
                operation_status['errors'] = results['errors']
                operation_status['completed_at'] = datetime.now().isoformat()
                
                logger.info(f"Ticket creation completed: {operation_id} - {results['successful']} successful, {results['failed']} failed")
            
        except Exception as e:
            logger.error(f"Background ticket creation error: {e}")
            self._update_operation_status(operation_id, 'failed', error=str(e))
    
    def _update_operation_status(self, operation_id: str, status: str, error: str = None):
        """
        Update operation status
        
        Args:
            operation_id (str): Operation ID
            status (str): New status
            error (str): Error message if any
        """
        operation_status = operation_status_store.get(operation_id)
        if operation_status:
            operation_status['status'] = status
            if error:
                operation_status['error'] = error
            operation_status['completed_at'] = datetime.now().isoformat()
    
    def get_operation_status(self, operation_id: str) -> Optional[Dict[str, Any]]:
        """
        Get operation status by ID
        
        Args:
            operation_id (str): Operation ID
            
        Returns:
            Optional[Dict[str, Any]]: Operation status or None if not found
        """
        return operation_status_store.get(operation_id)
    
    def cleanup_old_operations(self, max_age_hours: int = 24):
        """
        Clean up old operation status data
        
        Args:
            max_age_hours (int): Maximum age in hours
        """
        current_time = datetime.now()
        to_remove = []
        
        for operation_id, status in operation_status_store.items():
            started_at = datetime.fromisoformat(status['started_at'])
            age_hours = (current_time - started_at).total_seconds() / 3600
            
            if age_hours > max_age_hours:
                to_remove.append(operation_id)
        
        for operation_id in to_remove:
            del operation_status_store[operation_id]
            logger.info(f"Cleaned up old operation: {operation_id}")


class TicketSearchController:
    """
    Controller for handling ticket search and retrieval
    """
    
    def __init__(self):
        """Initialize the ticket search controller"""
        pass
    
    def get_ticket_details(self, ticket_key: str) -> Dict[str, Any]:
        """
        Get details of a specific ticket
        
        Args:
            ticket_key (str): Ticket key (e.g., 'PROJ-123')
            
        Returns:
            Dict[str, Any]: Ticket details or error response
        """
        try:
            # Validate ticket key format
            if not ticket_key or not isinstance(ticket_key, str):
                return create_error_response("Invalid ticket key")
            
            ticket_key = ticket_key.strip().upper()
            if not self._is_valid_ticket_key(ticket_key):
                return create_error_response("Invalid ticket key format")
            
            # Get Jira service
            jira_service = get_jira_service()
            if not jira_service:
                return create_error_response("Jira service not available")
            
            # Get ticket details
            success, ticket_data, error = jira_service.get_ticket_details(ticket_key)
            
            if success:
                return create_success_response(ticket_data)
            else:
                return create_error_response(f"Failed to retrieve ticket: {error}")
                
        except Exception as e:
            logger.error(f"Ticket search error: {e}")
            return create_error_response(f"Ticket search failed: {str(e)}")
    
    def _is_valid_ticket_key(self, ticket_key: str) -> bool:
        """
        Validate ticket key format
        
        Args:
            ticket_key (str): Ticket key to validate
            
        Returns:
            bool: True if valid format
        """
        import re
        # Jira ticket key format: PROJECT-123
        pattern = r'^[A-Z]+-\d+$'
        return bool(re.match(pattern, ticket_key))
    
    def search_tickets(self, jql: str, max_results: int = 50) -> Dict[str, Any]:
        """
        Search tickets using JQL
        
        Args:
            jql (str): JQL search query
            max_results (int): Maximum number of results
            
        Returns:
            Dict[str, Any]: Search results or error response
        """
        try:
            # Validate JQL
            if not jql or not isinstance(jql, str):
                return create_error_response("Invalid JQL query")
            
            jql = jql.strip()
            if len(jql) > 1000:
                return create_error_response("JQL query too long")
            
            # Get Jira service
            jira_service = get_jira_service()
            if not jira_service:
                return create_error_response("Jira service not available")
            
            # Search tickets
            success, search_results, error = jira_service.search_tickets(jql, max_results)
            
            if success:
                return create_success_response(search_results)
            else:
                return create_error_response(f"Search failed: {error}")
                
        except Exception as e:
            logger.error(f"Ticket search error: {e}")
            return create_error_response(f"Search failed: {str(e)}")


# Global controller instances
file_upload_controller = FileUploadController()
ticket_creation_controller = TicketCreationController()
ticket_search_controller = TicketSearchController()


def get_file_upload_controller() -> FileUploadController:
    """Get file upload controller instance"""
    return file_upload_controller


def get_ticket_creation_controller() -> TicketCreationController:
    """Get ticket creation controller instance"""
    return ticket_creation_controller


def get_ticket_search_controller() -> TicketSearchController:
    """Get ticket search controller instance"""
    return ticket_search_controller


def cleanup_old_data():
    """Clean up old data periodically"""
    try:
        file_upload_controller._cleanup_old_previews()
        ticket_creation_controller.cleanup_old_operations()
        logger.info("Cleanup completed")
    except Exception as e:
        logger.error(f"Cleanup error: {e}") 