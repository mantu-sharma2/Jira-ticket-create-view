
import webview
import threading
import sys
import os
from app import create_app

def start_flask_app():
    """Start Flask app in background thread"""
    app = create_app()
    app.run(host='127.0.0.1', port=4000, debug=False, use_reloader=False)

def main():
    """Main function to start desktop app"""
    # Start Flask app in background
    flask_thread = threading.Thread(target=start_flask_app, daemon=True)
    flask_thread.start()
    
    # Wait a moment for Flask to start
    import time
    time.sleep(2)
    
    # Create desktop window
    webview.create_window(
        title="Jira Ticket Manager",
        url="http://127.0.0.1:4000",
        width=1200,
        height=800,
        resizable=True,
        text_select=True,
        confirm_close=True
    )
    webview.start(debug=False)

if __name__ == "__main__":
    main()
