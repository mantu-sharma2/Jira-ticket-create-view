#!/usr/bin/env python3
"""
Simple build script for Jira Ticket Manager
Uses basic PyInstaller configuration to avoid bootloader issues
"""

import os
import sys
import subprocess
import platform
import shutil

def create_desktop_app():
    """Create desktop application using PyWebView"""
    desktop_app_code = '''
import webview
import threading
import time
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
'''
    
    with open("desktop_app.py", "w") as f:
        f.write(desktop_app_code)
    
    print("✓ Created desktop_app.py")

def build_executable():
    """Build executable using PyInstaller with simple configuration"""
    system = platform.system().lower()
    
    # Simple PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--name=JiraTicketManager",     # Executable name
        "--add-data=templates:templates",  # Include templates
        "--add-data=static:static",     # Include static files
        "--add-data=config.py:config.py",  # Include config
        "--hidden-import=flask",        # Include Flask
        "--hidden-import=flask_cors",   # Include CORS
        "--hidden-import=pandas",       # Include pandas
        "--hidden-import=requests",     # Include requests
        "--hidden-import=webview",      # Include webview
        "--hidden-import=threading",    # Include threading
        "--hidden-import=app",          # Include our app module
        "--hidden-import=routes",       # Include routes module
        "--hidden-import=controllers",  # Include controllers module
        "--hidden-import=jira_service", # Include jira_service module
        "--hidden-import=validation",   # Include validation module
        "--hidden-import=helpers",      # Include helpers module
        "--hidden-import=config",       # Include config module
        "desktop_app.py"                # Main script
    ]
    
    print(f"Building for {system}...")
    print("Command:", " ".join(cmd))
    
    try:
        subprocess.check_call(cmd)
        print("✓ Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

def create_distribution():
    """Create simple distribution package"""
    system = platform.system().lower()
    
    # Create distribution directory
    dist_dir = f"JiraTicketManager_{system.capitalize()}"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)
    
    print(f"Creating distribution package for {system}...")
    
    # Copy executable
    if system == "windows":
        exe_name = "dist/JiraTicketManager.exe"
    else:
        exe_name = "dist/JiraTicketManager"
    
    if os.path.exists(exe_name):
        shutil.copy2(exe_name, dist_dir)
        print(f"✓ Copied {exe_name}")
    else:
        print(f"❌ {exe_name} not found.")
        return False
    
    # Copy README
    if os.path.exists("APP_README.md"):
        shutil.copy2("APP_README.md", dist_dir)
        print("✓ Copied APP_README.md")
    
    # Copy sample Excel file
    if os.path.exists("sample_tickets.xlsx"):
        shutil.copy2("sample_tickets.xlsx", dist_dir)
        print("✓ Copied sample_tickets.xlsx")
    
    # Create simple README
    create_simple_readme(dist_dir, system)
    
    print(f"\n✅ Distribution package created: {dist_dir}")
    return True

def create_simple_readme(dist_dir, system):
    """Create simple README"""
    content = f'''# Jira Ticket Manager - {system.capitalize()}

## Quick Start

1. **Double-click** `JiraTicketManager` to run the application
2. **Configure** your Jira credentials when prompted
3. **Start creating** tickets from Excel files!

## What This App Does

- Upload Excel files with ticket data
- Create Jira tickets automatically
- View existing ticket details
- Real-time progress tracking

## Requirements

- {system.capitalize()} system
- Internet connection for Jira API
- Excel files with required columns (see APP_README.md)

## Support

See APP_README.md for detailed instructions and troubleshooting.

---
*Jira Ticket Manager v1.0*
'''
    
    with open(os.path.join(dist_dir, "README.md"), "w") as f:
        f.write(content)
    
    print("✓ Created README.md")

def cleanup():
    """Clean up build artifacts"""
    print("Cleaning up build artifacts...")
    
    # Files to remove
    files_to_remove = [
        "desktop_app.py",
        "JiraTicketManager.spec"
    ]
    
    # Directories to remove
    dirs_to_remove = [
        "build",
        "__pycache__"
    ]
    
    for file in files_to_remove:
        if os.path.exists(file):
            if os.path.isfile(file):
                os.remove(file)
                print(f"✓ Removed {file}")
            elif os.path.isdir(file):
                shutil.rmtree(file)
                print(f"✓ Removed {file}")
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ Removed {dir_name}")
    
    print("✅ Cleanup completed")

def main():
    """Main build function"""
    print("🚀 Jira Ticket Manager - Simple Build")
    print("=" * 40)
    
    # Create desktop app
    print("\n1. Creating desktop application...")
    create_desktop_app()
    
    # Build executable
    print("\n2. Building executable...")
    if build_executable():
        # Create distribution
        print("\n3. Creating distribution package...")
        create_distribution()
        
        # Cleanup
        print("\n4. Cleaning up...")
        cleanup()
        
        print("\n✅ Build completed successfully!")
        print("\n📁 Generated files:")
        system = platform.system().lower()
        print(f"  - JiraTicketManager_{system.capitalize()}/ (distribution folder)")
        print("  - dist/JiraTicketManager (executable)")
        
        print("\n📦 To distribute:")
        print(f"  - Share the JiraTicketManager_{system.capitalize()}/ folder")
        print("  - Or zip it for easy sharing")
        
        print("\n🎉 Your standalone app is ready!")
    else:
        print("\n❌ Build failed. Please check the error messages above.")

if __name__ == "__main__":
    main() 