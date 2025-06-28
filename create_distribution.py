#!/usr/bin/env python3
"""
Distribution script for Jira Ticket Manager
Creates packaged distributions for easy sharing with end users
"""

import os
import sys
import shutil
import zipfile
import platform
from pathlib import Path

def create_distribution_package():
    """Create distribution package with all necessary files"""
    system = platform.system().lower()
    
    # Create distribution directory
    dist_dir = f"JiraTicketManager_{system.capitalize()}"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)
    
    print(f"Creating distribution package for {system}...")
    
    # Copy executable
    if system == "windows":
        exe_name = "JiraTicketManager.exe"
        installer_name = "install.bat"
    else:
        exe_name = "JiraTicketManager"
        installer_name = "install.sh"
    
    if os.path.exists(exe_name):
        shutil.copy2(exe_name, dist_dir)
        print(f"✓ Copied {exe_name}")
    else:
        print(f"❌ {exe_name} not found. Please run build_app.py first.")
        return False
    
    # Copy installer
    if os.path.exists(installer_name):
        shutil.copy2(installer_name, dist_dir)
        print(f"✓ Copied {installer_name}")
    
    # Copy README
    if os.path.exists("APP_README.md"):
        shutil.copy2("APP_README.md", dist_dir)
        print("✓ Copied APP_README.md")
    
    # Copy sample Excel file
    if os.path.exists("sample_tickets.xlsx"):
        shutil.copy2("sample_tickets.xlsx", dist_dir)
        print("✓ Copied sample_tickets.xlsx")
    
    # Create system-specific README
    create_system_readme(dist_dir, system)
    
    # Create ZIP file
    zip_name = f"JiraTicketManager_{system.capitalize()}.zip"
    create_zip_package(dist_dir, zip_name)
    
    print(f"\n✅ Distribution package created: {zip_name}")
    return True

def create_system_readme(dist_dir, system):
    """Create system-specific README"""
    if system == "windows":
        content = '''# Jira Ticket Manager - Windows

## 🚀 Quick Start

1. **Extract the ZIP file** to a folder of your choice
2. **Double-click** `JiraTicketManager.exe` to run the application
3. **Or run** `install.bat` to install it to your system

## 📋 First Time Setup

1. Open the application
2. Configure your Jira credentials when prompted
3. Start creating tickets from Excel files!

## 🔧 Troubleshooting

- If the app won't start, try running as Administrator
- Make sure your antivirus isn't blocking the application
- Check that you have Windows 10 or later

## 📞 Support

See APP_README.md for detailed instructions and troubleshooting.
'''
    elif system == "darwin":
        content = '''# Jira Ticket Manager - macOS

## 🚀 Quick Start

1. **Extract the ZIP file** to a folder of your choice
2. **Double-click** `JiraTicketManager` to run the application
3. **Or run** `./install.sh` to install it to your system

## 📋 First Time Setup

1. Open the application
2. Configure your Jira credentials when prompted
3. Start creating tickets from Excel files!

## 🔧 Troubleshooting

- If you get a security warning, go to System Preferences > Security & Privacy and allow the app
- Make sure you have macOS 10.10 or later
- Try running from Terminal if double-click doesn't work

## 📞 Support

See APP_README.md for detailed instructions and troubleshooting.
'''
    else:  # Linux
        content = '''# Jira Ticket Manager - Linux

## 🚀 Quick Start

1. **Extract the ZIP file** to a folder of your choice
2. **Run** `./JiraTicketManager` to start the application
3. **Or run** `./install.sh` to install it to your system

## 📋 First Time Setup

1. Open the application
2. Configure your Jira credentials when prompted
3. Start creating tickets from Excel files!

## 🔧 Troubleshooting

- Make the file executable: `chmod +x JiraTicketManager`
- If you get permission errors, try running with sudo
- Make sure you have the required libraries installed

## 📞 Support

See APP_README.md for detailed instructions and troubleshooting.
'''
    
    with open(os.path.join(dist_dir, "QUICK_START.md"), "w") as f:
        f.write(content)
    
    print("✓ Created QUICK_START.md")

def create_zip_package(dist_dir, zip_name):
    """Create ZIP package"""
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, dist_dir)
                zipf.write(file_path, arcname)
    
    print(f"✓ Created {zip_name}")

def create_universal_package():
    """Create universal package with all platforms"""
    print("Creating universal distribution package...")
    
    # Create universal directory
    dist_dir = "JiraTicketManager_Universal"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)
    
    # Create platform subdirectories
    platforms = ["Windows", "macOS", "Linux"]
    for platform_name in platforms:
        platform_dir = os.path.join(dist_dir, platform_name)
        os.makedirs(platform_dir)
        
        # Copy platform-specific files if they exist
        if platform_name == "Windows":
            files_to_copy = ["JiraTicketManager.exe", "install.bat"]
        elif platform_name == "macOS":
            files_to_copy = ["JiraTicketManager", "install.sh"]
        else:  # Linux
            files_to_copy = ["JiraTicketManager", "install.sh"]
        
        for file in files_to_copy:
            if os.path.exists(file):
                shutil.copy2(file, platform_dir)
                print(f"✓ Copied {file} to {platform_name}")
    
    # Copy common files
    common_files = ["APP_README.md", "sample_tickets.xlsx"]
    for file in common_files:
        if os.path.exists(file):
            shutil.copy2(file, dist_dir)
            print(f"✓ Copied {file} to universal package")
    
    # Create universal README
    create_universal_readme(dist_dir)
    
    # Create ZIP
    zip_name = "JiraTicketManager_Universal.zip"
    create_zip_package(dist_dir, zip_name)
    
    print(f"\n✅ Universal package created: {zip_name}")

def create_universal_readme(dist_dir):
    """Create universal README"""
    content = '''# Jira Ticket Manager - Universal Package

This package contains the Jira Ticket Manager application for all supported platforms.

## 📁 Package Contents

- **Windows/** - Windows executable and installer
- **macOS/** - macOS executable and installer  
- **Linux/** - Linux executable and installer
- **APP_README.md** - Complete user documentation
- **sample_tickets.xlsx** - Sample Excel file for testing

## 🚀 Quick Start

1. **Choose your platform** folder (Windows, macOS, or Linux)
2. **Follow the instructions** in the platform-specific folder
3. **Read APP_README.md** for detailed usage instructions

## 📋 Platform-Specific Instructions

### Windows Users
1. Go to the `Windows` folder
2. Double-click `JiraTicketManager.exe`
3. Or run `install.bat` to install

### macOS Users
1. Go to the `macOS` folder
2. Double-click `JiraTicketManager`
3. Or run `./install.sh` to install

### Linux Users
1. Go to the `Linux` folder
2. Run `./JiraTicketManager`
3. Or run `./install.sh` to install

## 🔧 System Requirements

- **Windows**: Windows 10 or later
- **macOS**: macOS 10.10 or later
- **Linux**: Most modern distributions
- **Memory**: At least 512MB RAM
- **Storage**: At least 100MB free space
- **Network**: Internet connection for Jira API access

## 📞 Support

See APP_README.md for detailed instructions, troubleshooting, and support information.

---
*Jira Ticket Manager v1.0 - Cross-Platform Desktop Application*
'''
    
    with open(os.path.join(dist_dir, "README.md"), "w") as f:
        f.write(content)
    
    print("✓ Created universal README.md")

def main():
    """Main function"""
    print("📦 Jira Ticket Manager - Distribution Creator")
    print("=" * 50)
    
    # Check if build files exist
    required_files = ["JiraTicketManager", "JiraTicketManager.exe"]
    if not any(os.path.exists(f) for f in required_files):
        print("❌ No executable found. Please run build_app.py first.")
        print("   Run: python3 build_app.py")
        return
    
    # Create platform-specific package
    print("\n1. Creating platform-specific package...")
    if create_distribution_package():
        print("✅ Platform-specific package created successfully!")
    
    # Create universal package
    print("\n2. Creating universal package...")
    create_universal_package()
    
    print("\n🎉 Distribution packages created successfully!")
    print("\n📁 Generated packages:")
    
    system = platform.system().lower()
    if system == "windows":
        print("  - JiraTicketManager_Windows.zip")
    elif system == "darwin":
        print("  - JiraTicketManager_macOS.zip")
    else:
        print("  - JiraTicketManager_Linux.zip")
    
    print("  - JiraTicketManager_Universal.zip")
    
    print("\n📤 Ready to share with end users!")
    print("\n💡 Tips for distribution:")
    print("  - Send the ZIP file via email, cloud storage, or file sharing")
    print("  - Include the sample Excel file for testing")
    print("  - Provide the APP_README.md for user guidance")

if __name__ == "__main__":
    main() 