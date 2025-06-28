"""
Main Flask application for Jira Ticket Manager
Entry point for the application with modular architecture
"""

import logging
import os
from flask import Flask
from flask_cors import CORS

from routes import register_routes
from helpers import ensure_directory_exists

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app():
    """
    Create and configure Flask application
    
    Returns:
        Flask: Configured Flask application
    """
    # Create Flask app
    app = Flask(__name__)
    
    # Configure app
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Enable CORS
    CORS(app)
    
    # Ensure required directories exist
    ensure_directory_exists(app.config['UPLOAD_FOLDER'])
    ensure_directory_exists('logs')
    
    # Register routes
    register_routes(app)
    
    logger.info("Flask application created successfully")
    return app


def main():
    """Main function to run the Flask application"""
    app = create_app()
    
    # Import webbrowser here to avoid import issues
    import webbrowser
    import threading
    import time
    
    def open_browser():
        """Open browser after a short delay"""
        time.sleep(2)  # Wait for Flask to start
        webbrowser.open('http://127.0.0.1:4000')
    
    # Start browser in background thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Run the Flask app
    app.run(host='127.0.0.1', port=4000, debug=False)


if __name__ == "__main__":
    main() 