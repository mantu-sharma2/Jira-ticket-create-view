"""
Jira Ticket Manager - Flask Application
A clean, well-structured application for bulk Jira ticket creation from Excel files.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import requests
import os
import uuid
import base64
import threading
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app)

# Configuration
class Config:
    """Application configuration"""
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Jira Configuration
    JIRA_BASE_URL = os.environ.get('JIRA_BASE_URL', 'https://your-domain.atlassian.net')
    JIRA_API_TOKEN = os.environ.get('JIRA_API_TOKEN', 'your-api-token-here')
    JIRA_EMAIL = os.environ.get('JIRA_EMAIL', 'your-email@domain.com')
    DEFAULT_PROJECT_KEY = os.environ.get('DEFAULT_PROJECT_KEY', 'PROJ')

# Global storage (in production, use Redis or database)
class DataStore:
    """Simple in-memory data store for demo purposes"""
    def __init__(self):
        self.parsed_data: Dict[str, Dict] = {}
        self.operation_status: Dict[str, Dict] = {}
    
    def store_parsed_data(self, preview_id: str, data: Dict) -> None:
        """Store parsed Excel data"""
        self.parsed_data[preview_id] = {
            **data,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_parsed_data(self, preview_id: str) -> Optional[Dict]:
        """Get parsed data by preview ID"""
        return self.parsed_data.get(preview_id)
    
    def store_operation_status(self, operation_id: str, status: Dict) -> None:
        """Store operation status"""
        self.operation_status[operation_id] = status
    
    def get_operation_status(self, operation_id: str) -> Optional[Dict]:
        """Get operation status by ID"""
        return self.operation_status.get(operation_id)
    
    def cleanup_old_data(self) -> None:
        """Clean up old data to prevent memory leaks"""
        current_time = datetime.now()
        
        # Clean up parsed data older than 1 hour
        expired_previews = [
            preview_id for preview_id, data in self.parsed_data.items()
            if (current_time - datetime.fromisoformat(data['timestamp'])).total_seconds() > 3600
        ]
        for preview_id in expired_previews:
            del self.parsed_data[preview_id]
        
        # Clean up completed operations
        expired_operations = [
            op_id for op_id, data in self.operation_status.items()
            if data.get('status') == 'completed'
        ]
        for op_id in expired_operations:
            del self.operation_status[op_id]

# Initialize data store
data_store = DataStore()

# Ensure upload directory exists
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

class FileValidator:
    """File validation utilities"""
    
    @staticmethod
    def is_allowed_file(filename: str) -> bool:
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    
    @staticmethod
    def validate_excel_data(df: pd.DataFrame) -> Tuple[bool, str]:
        """Validate Excel data structure and content"""
        required_columns = ['summary', 'description', 'issue_type', 'priority']
        
        # Check for required columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return False, f"Missing required columns: {', '.join(missing_columns)}"
        
        # Check for empty required fields
        errors = []
        for col in required_columns:
            empty_rows = df[df[col].isnull() | (df[col] == '')].index.tolist()
            if empty_rows:
                errors.append(f"Column '{col}' has empty values in rows: {[i+1 for i in empty_rows]}")
        
        if errors:
            return False, "; ".join(errors)
        
        return True, "Data validation passed"

class JiraClient:
    """Jira API client"""
    
    def __init__(self):
        self.base_url = Config.JIRA_BASE_URL
        self.api_token = Config.JIRA_API_TOKEN
        self.email = Config.JIRA_EMAIL
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers"""
        credentials = f"{self.email}:{self.api_token}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        return {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def validate_config(self) -> Tuple[bool, str]:
        """Validate Jira configuration"""
        if not self.base_url or self.base_url == 'https://your-domain.atlassian.net':
            return False, "JIRA_BASE_URL not configured"
        if not self.api_token or self.api_token == 'your-api-token-here':
            return False, "JIRA_API_TOKEN not configured"
        if not self.email or self.email == 'your-email@domain.com':
            return False, "JIRA_EMAIL not configured"
        return True, "Configuration valid"
    
    def create_ticket(self, ticket_data: Dict) -> Dict:
        """Create a Jira ticket"""
        try:
            headers = self._get_auth_headers()
            
            # Prepare ticket payload
            payload = {
                "fields": {
                    "project": {
                        "key": ticket_data.get('project_key', Config.DEFAULT_PROJECT_KEY)
                    },
                    "summary": ticket_data['summary'],
                    "description": {
                        "type": "doc",
                        "version": 1,
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": ticket_data['description']
                                    }
                                ]
                            }
                        ]
                    },
                    "issuetype": {
                        "name": ticket_data['issue_type']
                    },
                    "priority": {
                        "name": ticket_data['priority']
                    }
                }
            }
            
            # Add optional fields
            if ticket_data.get('assignee'):
                payload["fields"]["assignee"] = {"name": ticket_data['assignee']}
            
            if ticket_data.get('labels'):
                payload["fields"]["labels"] = ticket_data['labels'].split(',')
            
            response = requests.post(
                f"{self.base_url}/rest/api/3/issue",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 201:
                result = response.json()
                return {
                    'success': True,
                    'ticket_id': result['key'],
                    'ticket_url': f"{self.base_url}/browse/{result['key']}"
                }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            logger.error(f"Error creating Jira ticket: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_ticket(self, ticket_id: str) -> Dict:
        """Get Jira ticket details"""
        try:
            headers = self._get_auth_headers()
            
            response = requests.get(
                f"{self.base_url}/rest/api/3/issue/{ticket_id}",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return {'success': True, 'data': response.json()}
            else:
                return {'success': False, 'error': f"HTTP {response.status_code}: {response.text}"}
                
        except Exception as e:
            logger.error(f"Error fetching Jira ticket: {str(e)}")
            return {'success': False, 'error': str(e)}

# Initialize Jira client
jira_client = JiraClient()

class TicketProcessor:
    """Handle ticket creation processing"""
    
    @staticmethod
    def process_tickets(operation_id: str, ticket_data: List[Dict]) -> None:
        """Process tickets in background thread"""
        logger.info(f"Starting ticket processing for operation {operation_id}")
        
        for index, row in enumerate(ticket_data):
            ticket_operation_id = f"{operation_id}_{index}"
            
            # Update status to processing
            data_store.operation_status[operation_id]['results'].append({
                'row': index + 1,
                'summary': row['summary'],
                'status': 'processing'
            })
            
            # Create ticket
            result = jira_client.create_ticket(row)
            
            # Update progress
            if result['success']:
                data_store.operation_status[operation_id]['completed'] += 1
                data_store.operation_status[operation_id]['results'][index]['status'] = 'completed'
                data_store.operation_status[operation_id]['results'][index]['result'] = result
            else:
                data_store.operation_status[operation_id]['failed'] += 1
                data_store.operation_status[operation_id]['results'][index]['status'] = 'failed'
                data_store.operation_status[operation_id]['results'][index]['result'] = result
            
            # Clean up individual operation status
            if ticket_operation_id in data_store.operation_status:
                del data_store.operation_status[ticket_operation_id]
        
        # Mark operation as completed
        data_store.operation_status[operation_id]['status'] = 'completed'
        logger.info(f"Completed ticket processing for operation {operation_id}")

# Routes
@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and parsing"""
    logger.info("File upload request received")
    
    # Clean up old data
    data_store.cleanup_old_data()
    
    # Validate request
    if 'file' not in request.files:
        logger.warning("No file in request")
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        logger.warning("Empty filename")
        return jsonify({'error': 'No file selected'}), 400
    
    if not FileValidator.is_allowed_file(file.filename):
        logger.warning(f"Invalid file type: {file.filename}")
        return jsonify({'error': 'Invalid file type. Please upload Excel files only.'}), 400
    
    try:
        logger.info(f"Processing file: {file.filename}")
        
        # Read Excel file
        df = pd.read_excel(file)
        logger.info(f"Excel file read successfully. Shape: {df.shape}")
        logger.info(f"Columns: {df.columns.tolist()}")
        
        # Validate data
        is_valid, message = FileValidator.validate_excel_data(df)
        logger.info(f"Validation result: {is_valid}, Message: {message}")
        
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Generate preview ID and store data
        preview_id = str(uuid.uuid4())
        logger.info(f"Generated preview ID: {preview_id}")
        
        parsed_data = {
            'data': df.to_dict('records'),
            'columns': df.columns.tolist(),
            'total_rows': len(df)
        }
        
        data_store.store_parsed_data(preview_id, parsed_data)
        
        # Prepare response
        response_data = {
            'success': True,
            'preview_id': preview_id,
            'total_rows': len(df),
            'columns': df.columns.tolist(),
            'data': df.to_dict('records')[:10]  # First 10 rows for preview
        }
        
        logger.info("File upload successful")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route('/preview/<preview_id>')
def get_preview(preview_id: str):
    """Get full preview data"""
    data = data_store.get_parsed_data(preview_id)
    if not data:
        return jsonify({'error': 'Preview not found'}), 404
    
    return jsonify({
        'success': True,
        'data': data['data'],
        'columns': data['columns'],
        'total_rows': data['total_rows']
    })

@app.route('/create-tickets', methods=['POST'])
def create_tickets():
    """Create tickets from preview data"""
    logger.info("Ticket creation request received")
    
    # Validate Jira configuration
    config_valid, config_error = jira_client.validate_config()
    if not config_valid:
        logger.error(f"Jira configuration error: {config_error}")
        return jsonify({'error': f'Jira configuration error: {config_error}. Please check your configuration.'}), 400
    
    # Get request data
    data = request.get_json()
    preview_id = data.get('preview_id')
    
    if not preview_id:
        return jsonify({'error': 'Preview ID is required'}), 400
    
    # Get parsed data
    parsed_data = data_store.get_parsed_data(preview_id)
    if not parsed_data:
        return jsonify({'error': 'Preview not found'}), 404
    
    ticket_data = parsed_data['data']
    
    # Generate operation ID and initialize status
    operation_id = str(uuid.uuid4())
    logger.info(f"Starting ticket creation operation: {operation_id}")
    
    data_store.store_operation_status(operation_id, {
        'status': 'processing',
        'total_tickets': len(ticket_data),
        'completed': 0,
        'failed': 0,
        'results': []
    })
    
    # Start background processing
    thread = threading.Thread(
        target=TicketProcessor.process_tickets,
        args=(operation_id, ticket_data)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'operation_id': operation_id,
        'total_tickets': len(ticket_data)
    })

@app.route('/status/<operation_id>')
def get_status(operation_id: str):
    """Get operation status"""
    status = data_store.get_operation_status(operation_id)
    if not status:
        return jsonify({'error': 'Operation not found'}), 404
    
    return jsonify(status)

@app.route('/ticket/<ticket_id>')
def get_ticket(ticket_id: str):
    """Get Jira ticket details"""
    # Validate Jira configuration
    config_valid, config_error = jira_client.validate_config()
    if not config_valid:
        return jsonify({'error': f'Jira configuration error: {config_error}. Please check your configuration.'}), 400
    
    if not ticket_id or not ticket_id.strip():
        return jsonify({'error': 'Ticket ID is required'}), 400
    
    result = jira_client.get_ticket(ticket_id.strip())
    return jsonify(result)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("Starting Jira Ticket Manager application")
    app.run(debug=True, host='0.0.0.0', port=4000) 