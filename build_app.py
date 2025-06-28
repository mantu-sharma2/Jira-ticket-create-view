#!/usr/bin/env python3
"""
Build script for creating standalone Jira Ticket Manager application
Creates executable files for Windows and macOS
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed successfully")
    
    try:
        import webview
        print("✓ PyWebView is installed")
    except ImportError:
        print("❌ PyWebView not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pywebview"])
        print("✓ PyWebView installed successfully")

def create_desktop_app():
    """Create desktop application using PyWebView"""
    desktop_app_code = '''
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
'''
    
    with open("desktop_app.py", "w") as f:
        f.write(desktop_app_code)
    
    print("✓ Created desktop_app.py")

def build_executable():
    """Build executable using PyInstaller"""
    system = platform.system().lower()
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window (Windows/macOS)
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
        "--hidden-import=uuid",         # Include uuid
        "--hidden-import=datetime",     # Include datetime
        "--hidden-import=logging",      # Include logging
        "--hidden-import=os",           # Include os
        "--hidden-import=sys",          # Include sys
        "--hidden-import=json",         # Include json
        "--hidden-import=base64",       # Include base64
        "--hidden-import=re",           # Include re
        "--hidden-import=time",         # Include time
        "--hidden-import=pathlib",      # Include pathlib
        "--hidden-import=werkzeug",     # Include werkzeug
        "--hidden-import=jinja2",       # Include jinja2
        "--hidden-import=markupsafe",   # Include markupsafe
        "--hidden-import=itsdangerous", # Include itsdangerous
        "--hidden-import=click",        # Include click
        "--hidden-import=blinker",      # Include blinker
        "--hidden-import=six",          # Include six
        "--hidden-import=urllib3",      # Include urllib3
        "--hidden-import=certifi",      # Include certifi
        "--hidden-import=charset_normalizer", # Include charset_normalizer
        "--hidden-import=idna",         # Include idna
        "--hidden-import=openpyxl",     # Include openpyxl
        "--hidden-import=et_xmlfile",   # Include et_xmlfile
        "--hidden-import=jdcal",        # Include jdcal
        "--hidden-import=python_dateutil", # Include python_dateutil
        "--hidden-import=pytz",         # Include pytz
        "--hidden-import=numpy",        # Include numpy
        "--hidden-import=six",          # Include six
        "--hidden-import=app",          # Include our app module
        "--hidden-import=routes",       # Include routes module
        "--hidden-import=controllers",  # Include controllers module
        "--hidden-import=jira_service", # Include jira_service module
        "--hidden-import=validation",   # Include validation module
        "--hidden-import=helpers",      # Include helpers module
        "--hidden-import=config",       # Include config module
        "desktop_app.py"                # Main script
    ]
    
    # Add system-specific options
    if system == "darwin":  # macOS
        pass  # No extra flags for local build
    elif system == "windows":
        cmd.extend([
            "--icon=app_icon.ico",              # Windows icon (if available)
        ])
    
    print(f"Building for {system}...")
    print("Command:", " ".join(cmd))
    
    try:
        subprocess.check_call(cmd)
        print("✓ Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

def create_installer_script():
    """Create installer script for easy setup"""
    installer_script = '''#!/bin/bash
# Jira Ticket Manager - Installer Script

echo "Installing Jira Ticket Manager..."

# Create application directory
APP_DIR="$HOME/JiraTicketManager"
mkdir -p "$APP_DIR"

# Copy executable
cp JiraTicketManager "$APP_DIR/"

# Make executable
chmod +x "$APP_DIR/JiraTicketManager"

# Create desktop shortcut (Linux/macOS)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    cat > "$HOME/.local/share/applications/jira-ticket-manager.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Jira Ticket Manager
Comment=Create Jira tickets from Excel files
Exec=$APP_DIR/JiraTicketManager
Icon=$APP_DIR/JiraTicketManager
Terminal=false
Categories=Office;
EOF
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS - create .app bundle
    mkdir -p "$APP_DIR/JiraTicketManager.app/Contents/MacOS"
    mkdir -p "$APP_DIR/JiraTicketManager.app/Contents/Resources"
    
    cp JiraTicketManager "$APP_DIR/JiraTicketManager.app/Contents/MacOS/"
    
    cat > "$APP_DIR/JiraTicketManager.app/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>JiraTicketManager</string>
    <key>CFBundleIdentifier</key>
    <string>com.jiraticketmanager.app</string>
    <key>CFBundleName</key>
    <string>Jira Ticket Manager</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.10</string>
</dict>
</plist>
EOF
fi

echo "Installation completed!"
echo "Application installed to: $APP_DIR"
echo ""
echo "To run the application:"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "  - Use the desktop shortcut, or"
    echo "  - Run: $APP_DIR/JiraTicketManager"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "  - Double-click JiraTicketManager.app, or"
    echo "  - Run: open $APP_DIR/JiraTicketManager.app"
fi
'''
    
    with open("install.sh", "w") as f:
        f.write(installer_script)
    
    # Make executable
    os.chmod("install.sh", 0o755)
    print("✓ Created install.sh")

def create_windows_installer():
    """Create Windows batch installer"""
    windows_installer = '''@echo off
REM Jira Ticket Manager - Windows Installer

echo Installing Jira Ticket Manager...

REM Create application directory
set APP_DIR=%USERPROFILE%\\JiraTicketManager
if not exist "%APP_DIR%" mkdir "%APP_DIR%"

REM Copy executable
copy "JiraTicketManager.exe" "%APP_DIR%\\"

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Jira Ticket Manager.lnk'); $Shortcut.TargetPath = '%APP_DIR%\\JiraTicketManager.exe'; $Shortcut.Save()"

echo Installation completed!
echo Application installed to: %APP_DIR%
echo.
echo To run the application:
echo   - Double-click the desktop shortcut, or
echo   - Run: %APP_DIR%\\JiraTicketManager.exe
pause
'''
    
    with open("install.bat", "w") as f:
        f.write(windows_installer)
    
    print("✓ Created install.bat")

def create_readme():
    """Create user-friendly README for the app"""
    readme_content = '''# Jira Ticket Manager - Desktop Application

## 🚀 Quick Start

### For Windows Users:
1. Double-click `JiraTicketManager.exe` to run the application
2. Or run `install.bat` to install it to your system

### For macOS Users:
1. Double-click `JiraTicketManager` to run the application
2. Or run `./install.sh` to install it to your system

### For Linux Users:
1. Run `./JiraTicketManager` to start the application
2. Or run `./install.sh` to install it to your system

## 📋 What This App Does

This application helps you create Jira tickets from Excel files. Here's how to use it:

### Step 1: Prepare Your Excel File
Your Excel file should have these columns:
- **summary** (required): Ticket title
- **description** (required): Detailed description
- **issue_type** (required): Type of issue (bug, task, story, etc.)
- **priority** (required): Priority level (high, medium, low, etc.)
- **project_key** (optional): Jira project key
- **assignee** (optional): Username to assign the ticket to
- **labels** (optional): Comma-separated labels

### Step 2: Configure Jira Settings
Before using the app, you need to set up your Jira credentials:
1. Open the application
2. Go to the "Upload & Create Tickets" tab
3. The app will guide you through the setup process

### Step 3: Upload and Create Tickets
1. Click "Choose File" and select your Excel file
2. Review the preview of your data
3. Click "Create Tickets" to start the process
4. Monitor the progress as tickets are created

### Step 4: View Existing Tickets
1. Switch to the "View Ticket Details" tab
2. Enter a ticket ID (e.g., PROJ-123)
3. View detailed information about the ticket

## 🔧 Troubleshooting

### Common Issues:

**App won't start:**
- Make sure you have the correct version for your operating system
- Try running as administrator (Windows) or with sudo (Linux/macOS)

**Can't connect to Jira:**
- Check your internet connection
- Verify your Jira credentials are correct
- Ensure your Jira instance is accessible

**Excel file errors:**
- Make sure your Excel file has the required columns
- Check that required fields are not empty
- Verify the file format is .xlsx or .xls

**Permission errors:**
- Make sure you have write permissions in the application directory
- Try running the application as administrator

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Contact your system administrator
3. Refer to the main project documentation

## 🔒 Security Notes

- The application stores your Jira credentials locally
- Keep your API tokens secure and don't share them
- The application only connects to your specified Jira instance

## 📝 System Requirements

- **Windows**: Windows 10 or later
- **macOS**: macOS 10.10 or later
- **Linux**: Most modern distributions
- **Memory**: At least 512MB RAM
- **Storage**: At least 100MB free space
- **Network**: Internet connection for Jira API access

---
*Jira Ticket Manager v1.0 - Built with Python and Flask*
'''
    
    with open("APP_README.md", "w") as f:
        f.write(readme_content)
    
    print("✓ Created APP_README.md")

def cleanup():
    """Clean up build artifacts"""
    print("Cleaning up build artifacts...")
    
    # Remove build directories
    for dir_name in ["build", "__pycache__"]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ Removed {dir_name}")
    
    # Remove spec file
    if os.path.exists("JiraTicketManager.spec"):
        os.remove("JiraTicketManager.spec")
        print("✓ Removed JiraTicketManager.spec")

def main():
    """Main build function"""
    print("🚀 Jira Ticket Manager - Build Script")
    print("=" * 50)
    
    # Check dependencies
    print("\n1. Checking dependencies...")
    check_dependencies()
    
    # Create desktop app
    print("\n2. Creating desktop application...")
    create_desktop_app()
    
    # Build executable
    print("\n3. Building executable...")
    if build_executable():
        # Create installers
        print("\n4. Creating installers...")
        create_installer_script()
        create_windows_installer()
        
        # Create README
        print("\n5. Creating user documentation...")
        create_readme()
        
        # Cleanup
        print("\n6. Cleaning up...")
        cleanup()
        
        print("\n✅ Build completed successfully!")
        print("\n📁 Generated files:")
        print("  - JiraTicketManager (executable)")
        print("  - install.sh (Linux/macOS installer)")
        print("  - install.bat (Windows installer)")
        print("  - APP_README.md (user guide)")
        
        print("\n📦 To distribute:")
        system = platform.system().lower()
        if system == "darwin":
            print("  - Copy JiraTicketManager to macOS users")
        elif system == "windows":
            print("  - Copy JiraTicketManager.exe to Windows users")
        else:
            print("  - Copy JiraTicketManager to Linux users")
        
        print("\n🎉 Your standalone app is ready!")
    else:
        print("\n❌ Build failed. Please check the error messages above.")

if __name__ == "__main__":
    main() 