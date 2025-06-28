"""
Jira Service for Jira Ticket Manager
Handles all Jira API interactions and ticket creation logic
"""

import logging
import requests
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import time
from config import JIRA_CONFIG
from helpers import create_error_response, create_success_response, format_timestamp

# Configure logging
logger = logging.getLogger(__name__)


class JiraService:
    """
    Service class for handling Jira API operations
    """
    
    def __init__(self):
        """Initialize Jira service with configuration"""
        self.base_url = JIRA_CONFIG.get('JIRA_BASE_URL')
        self.username = JIRA_CONFIG.get('JIRA_USERNAME')
        self.api_token = JIRA_CONFIG.get('JIRA_API_TOKEN')
        self.project_key = JIRA_CONFIG.get('JIRA_PROJECT_KEY')
        
        # Validate configuration
        if not all([self.base_url, self.username, self.api_token]):
            logger.error("Jira configuration incomplete")
            raise ValueError("Jira configuration is incomplete. Please check config.py")
    
    def _get_headers(self) -> Dict[str, str]:
        """
        Get headers for Jira API requests
        
        Returns:
            Dict[str, str]: Headers dictionary
        """
        import base64
        credentials = f"{self.username}:{self.api_token}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        return {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Tuple[bool, Any, str]:
        """
        Make HTTP request to Jira API
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint
            data (Optional[Dict]): Request data
            
        Returns:
            Tuple[bool, Any, str]: (success, response_data, error_message)
        """
        try:
            url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
            headers = self._get_headers()
            
            logger.info(f"Making {method} request to {url}")
            
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=30)
            else:
                return False, None, f"Unsupported HTTP method: {method}"
            
            if response.status_code in [200, 201]:
                return True, response.json(), ""
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                logger.error(error_msg)
                return False, None, error_msg
                
        except requests.exceptions.Timeout:
            error_msg = "Request timeout"
            logger.error(error_msg)
            return False, None, error_msg
        except requests.exceptions.ConnectionError:
            error_msg = "Connection error - check Jira URL and network"
            logger.error(error_msg)
            return False, None, error_msg
        except Exception as e:
            error_msg = f"Request failed: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg
    
    def test_connection(self) -> Tuple[bool, str]:
        """
        Test connection to Jira API
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            success, data, error = self._make_request('GET', '/rest/api/2/myself')
            if success:
                user_info = data.get('displayName', 'Unknown')
                return True, f"Connected successfully as {user_info}"
            else:
                return False, f"Connection failed: {error}"
        except Exception as e:
            return False, f"Connection test failed: {str(e)}"
    
    def get_project_info(self, project_key: Optional[str] = None) -> Tuple[bool, Any, str]:
        """
        Get project information from Jira
        
        Args:
            project_key (Optional[str]): Project key to get info for
            
        Returns:
            Tuple[bool, Any, str]: (success, project_data, error_message)
        """
        project = project_key or self.project_key
        if not project:
            return False, None, "No project key specified"
        
        return self._make_request('GET', f'/rest/api/2/project/{project}')
    
    def create_ticket(self, ticket_data: Dict[str, Any]) -> Tuple[bool, Any, str]:
        """
        Create a single ticket in Jira
        
        Args:
            ticket_data (Dict[str, Any]): Ticket data dictionary
            
        Returns:
            Tuple[bool, Any, str]: (success, ticket_info, error_message)
        """
        try:
            # Prepare ticket payload
            payload = self._prepare_ticket_payload(ticket_data)
            
            # Make API request
            success, response_data, error = self._make_request('POST', '/rest/api/2/issue', payload)
            
            if success:
                ticket_key = response_data.get('key')
                ticket_id = response_data.get('id')
                logger.info(f"Created ticket: {ticket_key} (ID: {ticket_id})")
                return True, response_data, ""
            else:
                return False, None, error
                
        except Exception as e:
            error_msg = f"Failed to create ticket: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg
    
    def _prepare_ticket_payload(self, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare ticket data for Jira API
        
        Args:
            ticket_data (Dict[str, Any]): Raw ticket data
            
        Returns:
            Dict[str, Any]: Formatted payload for Jira API
        """
        # Map issue types to Jira issue types
        issue_type_mapping = {
            'bug': 'Bug',
            'task': 'Task',
            'story': 'Story',
            'epic': 'Epic',
            'subtask': 'Sub-task'
        }
        
        # Map priorities to Jira priority names
        priority_mapping = {
            'low': 'Low',
            'medium': 'Medium',
            'high': 'High',
            'critical': 'Critical',
            'highest': 'Highest'
        }
        
        # Get values with defaults
        summary = str(ticket_data.get('summary', '')).strip()
        description = str(ticket_data.get('description', '')).strip()
        issue_type = str(ticket_data.get('issue_type', '')).lower().strip()
        priority = str(ticket_data.get('priority', '')).lower().strip()
        project_key = str(ticket_data.get('project_key', self.project_key)).strip()
        assignee = str(ticket_data.get('assignee', '')).strip()
        labels = str(ticket_data.get('labels', '')).strip()
        
        # Prepare labels list
        labels_list = []
        if labels:
            labels_list = [label.strip() for label in labels.split(',') if label.strip()]
        
        # Build payload
        payload = {
            "fields": {
                "project": {
                    "key": project_key
                },
                "summary": summary,
                "description": description,
                "issuetype": {
                    "name": issue_type_mapping.get(issue_type, 'Task')
                },
                "priority": {
                    "name": priority_mapping.get(priority, 'Medium')
                }
            }
        }
        
        # Add optional fields
        if assignee:
            payload["fields"]["assignee"] = {
                "name": assignee
            }
        
        if labels_list:
            payload["fields"]["labels"] = labels_list
        
        return payload
    
    def get_ticket_details(self, ticket_key: str) -> Tuple[bool, Any, str]:
        """
        Get details of a specific ticket
        
        Args:
            ticket_key (str): Ticket key (e.g., 'PROJ-123')
            
        Returns:
            Tuple[bool, Any, str]: (success, ticket_data, error_message)
        """
        return self._make_request('GET', f'/rest/api/2/issue/{ticket_key}')
    
    # def update_ticket(self, ticket_key: str, update_data: Dict[str, Any]) -> Tuple[bool, Any, str]:
    #     """
    #     Update an existing ticket
        
    #     Args:
    #         ticket_key (str): Ticket key to update
    #         update_data (Dict[str, Any]): Data to update
            
    #     Returns:
    #         Tuple[bool, Any, str]: (success, response_data, error_message)
    #     """
    #     return self._make_request('PUT', f'/rest/api/2/issue/{ticket_key}', update_data)
    
    # def delete_ticket(self, ticket_key: str) -> Tuple[bool, str]:
    #     """
    #     Delete a ticket (if permissions allow)
        
    #     Args:
    #         ticket_key (str): Ticket key to delete
            
    #     Returns:
    #         Tuple[bool, str]: (success, error_message)
    #     """
    #     success, _, error = self._make_request('DELETE', f'/rest/api/2/issue/{ticket_key}')
    #     return success, error
    
    def search_tickets(self, jql: str, max_results: int = 50) -> Tuple[bool, Any, str]:
        """
        Search tickets using JQL
        
        Args:
            jql (str): JQL search query
            max_results (int): Maximum number of results
            
        Returns:
            Tuple[bool, Any, str]: (success, search_results, error_message)
        """
        search_data = {
            "jql": jql,
            "maxResults": max_results,
            "fields": ["summary", "description", "status", "priority", "assignee", "created", "updated"]
        }
        
        return self._make_request('POST', '/rest/api/2/search', search_data)
    
    def get_issue_types(self) -> Tuple[bool, Any, str]:
        """
        Get available issue types for the project
        
        Returns:
            Tuple[bool, Any, str]: (success, issue_types, error_message)
        """
        return self._make_request('GET', f'/rest/api/2/project/{self.project_key}')
    
    def get_priorities(self) -> Tuple[bool, Any, str]:
        """
        Get available priorities
        
        Returns:
            Tuple[bool, Any, str]: (success, priorities, error_message)
        """
        return self._make_request('GET', '/rest/api/2/priority')
    
    def create_multiple_tickets(self, tickets_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create multiple tickets with progress tracking
        
        Args:
            tickets_data (List[Dict[str, Any]]): List of ticket data dictionaries
            
        Returns:
            Dict[str, Any]: Results summary
        """
        results = {
            'total': len(tickets_data),
            'successful': 0,
            'failed': 0,
            'tickets': [],
            'errors': []
        }
        
        for index, ticket_data in enumerate(tickets_data):
            try:
                logger.info(f"Creating ticket {index + 1}/{len(tickets_data)}")
                
                success, ticket_info, error = self.create_ticket(ticket_data)
                
                if success:
                    results['successful'] += 1
                    results['tickets'].append({
                        'index': index,
                        'key': ticket_info.get('key'),
                        'id': ticket_info.get('id'),
                        'summary': ticket_data.get('summary'),
                        'status': 'created'
                    })
                    logger.info(f"Created ticket: {ticket_info.get('key')} (ID: {ticket_info.get('id')})")
                else:
                    results['failed'] += 1
                    results['errors'].append({
                        'index': index,
                        'summary': ticket_data.get('summary'),
                        'error': error
                    })
                    logger.error(f"Error creating ticket {index + 1}: {e}")
                
                # Add small delay to avoid rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                results['failed'] += 1
                results['errors'].append({
                    'index': index,
                    'summary': ticket_data.get('summary'),
                    'error': str(e)
                })
                logger.error(f"Error creating ticket {index + 1}: {e}")
        
        logger.info(f"Ticket creation completed: {results['successful']} successful, {results['failed']} failed")
        return results


# Global Jira service instance
jira_service = None


def get_jira_service() -> Optional[JiraService]:
    """
    Get or create Jira service instance
    
    Returns:
        Optional[JiraService]: Jira service instance or None if configuration is invalid
    """
    global jira_service
    
    if jira_service is None:
        try:
            jira_service = JiraService()
        except ValueError as e:
            logger.error(f"Failed to initialize Jira service: {e}")
            return None
    
    return jira_service


def validate_jira_config() -> Tuple[bool, str]:
    """
    Validate Jira configuration
    
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    try:
        service = get_jira_service()
        if service is None:
            return False, "Jira configuration is invalid"
        
        return service.test_connection()
    except Exception as e:
        return False, f"Configuration validation failed: {str(e)}" 