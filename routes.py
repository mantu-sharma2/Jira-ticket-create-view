"""
Routes for Jira Ticket Manager
Contains all Flask routes and HTTP request handlers
"""

import logging
from flask import request, jsonify, render_template
from werkzeug.utils import secure_filename
import os

from controllers import (
    get_file_upload_controller, get_ticket_creation_controller, get_ticket_search_controller
)
from helpers import create_error_response, create_success_response
from jira_service import validate_jira_config

# Configure logging
logger = logging.getLogger(__name__)


def register_routes(app):
    """
    Register all routes with the Flask app
    
    Args:
        app: Flask application instance
    """
    
    @app.route('/')
    def index():
        """
        Serve the main application page
        
        Returns:
            str: Rendered HTML template
        """
        return render_template('index.html')
    
    @app.route('/api/upload', methods=['POST'])
    def upload_file():
        """
        Handle file upload and return preview data
        
        Returns:
            JSON: Upload result with preview data or error
        """
        try:
            # Check if file was uploaded
            if 'file' not in request.files:
                return jsonify(create_error_response("No file uploaded"))
            
            file = request.files['file']
            
            # Check if file was selected
            if file.filename == '':
                return jsonify(create_error_response("No file selected"))
            
            # Process file upload
            controller = get_file_upload_controller()
            result = controller.process_file_upload(file)
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Upload route error: {e}")
            return jsonify(create_error_response(f"Upload failed: {str(e)}"))
    
    @app.route('/api/create-tickets', methods=['POST'])
    def create_tickets():
        """
        Start ticket creation process
        
        Returns:
            JSON: Operation result with operation ID or error
        """
        try:
            data = request.get_json()
            if not data or 'preview_id' not in data:
                return jsonify(create_error_response("Preview ID is required"))
            
            preview_id = data['preview_id']
            
            # Start ticket creation
            controller = get_ticket_creation_controller()
            result = controller.start_ticket_creation(preview_id)
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Create tickets route error: {e}")
            return jsonify(create_error_response(f"Failed to start ticket creation: {str(e)}"))
    
    @app.route('/api/status/<operation_id>')
    def get_status(operation_id):
        """
        Get operation status by ID
        
        Args:
            operation_id (str): Operation ID from URL
            
        Returns:
            JSON: Operation status or error
        """
        try:
            controller = get_ticket_creation_controller()
            status = controller.get_operation_status(operation_id)
            
            if status:
                return jsonify(create_success_response(status))
            else:
                return jsonify(create_error_response("Operation not found"))
                
        except Exception as e:
            logger.error(f"Status route error: {e}")
            return jsonify(create_error_response(f"Failed to get status: {str(e)}"))
    
    @app.route('/api/ticket/<ticket_key>')
    def get_ticket(ticket_key):
        """
        Get ticket details by ticket key
        
        Args:
            ticket_key (str): Ticket key from URL
            
        Returns:
            JSON: Ticket details or error
        """
        try:
            controller = get_ticket_search_controller()
            result = controller.get_ticket_details(ticket_key)
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Get ticket route error: {e}")
            return jsonify(create_error_response(f"Failed to get ticket: {str(e)}"))
    
    @app.route('/api/search', methods=['POST'])
    def search_tickets():
        """
        Search tickets using JQL
        
        Returns:
            JSON: Search results or error
        """
        try:
            data = request.get_json()
            if not data or 'jql' not in data:
                return jsonify(create_error_response("JQL query is required"))
            
            jql = data['jql']
            max_results = data.get('max_results', 50)
            
            controller = get_ticket_search_controller()
            result = controller.search_tickets(jql, max_results)
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Search route error: {e}")
            return jsonify(create_error_response(f"Search failed: {str(e)}"))
    
    @app.route('/api/health')
    def health_check():
        """
        Health check endpoint
        
        Returns:
            JSON: Health status
        """
        try:
            # Check Jira configuration
            is_valid, message = validate_jira_config()
            
            health_status = {
                'status': 'healthy' if is_valid else 'unhealthy',
                'jira_connection': message,
                'timestamp': create_success_response()['timestamp']
            }
            
            return jsonify(create_success_response(health_status))
            
        except Exception as e:
            logger.error(f"Health check error: {e}")
            return jsonify(create_error_response(f"Health check failed: {str(e)}"))
    
    @app.route('/api/config/validate')
    def validate_config():
        """
        Validate Jira configuration
        
        Returns:
            JSON: Configuration validation result
        """
        try:
            is_valid, message = validate_jira_config()
            
            if is_valid:
                return jsonify(create_success_response({
                    'valid': True,
                    'message': message
                }))
            else:
                return jsonify(create_error_response(message))
                
        except Exception as e:
            logger.error(f"Config validation error: {e}")
            return jsonify(create_error_response(f"Configuration validation failed: {str(e)}"))
    
    @app.route('/api/cleanup', methods=['POST'])
    def cleanup_data():
        """
        Clean up old data
        
        Returns:
            JSON: Cleanup result
        """
        try:
            from controllers import cleanup_old_data
            cleanup_old_data()
            
            return jsonify(create_success_response("Cleanup completed"))
            
        except Exception as e:
            logger.error(f"Cleanup route error: {e}")
            return jsonify(create_error_response(f"Cleanup failed: {str(e)}"))
    
    @app.errorhandler(404)
    def not_found(error):
        """
        Handle 404 errors
        
        Args:
            error: Error object
            
        Returns:
            JSON: Error response
        """
        return jsonify(create_error_response("Endpoint not found", 404)), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """
        Handle 500 errors
        
        Args:
            error: Error object
            
        Returns:
            JSON: Error response
        """
        logger.error(f"Internal server error: {error}")
        return jsonify(create_error_response("Internal server error", 500)), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """
        Handle unhandled exceptions
        
        Args:
            error: Exception object
            
        Returns:
            JSON: Error response
        """
        logger.error(f"Unhandled exception: {error}")
        return jsonify(create_error_response("An unexpected error occurred", 500)), 500
    
    # Log registered routes
    logger.info("Routes registered successfully")
    for rule in app.url_map.iter_rules():
        logger.info(f"Route: {rule.rule} -> {rule.endpoint}") 