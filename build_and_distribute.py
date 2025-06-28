#!/usr/bin/env python3
"""
One-click build and distribution script for Jira Ticket Manager
Handles the entire process from building to creating distribution packages
"""

import os
import sys
import subprocess
import platform
import time

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        if result.stdout:
            print("Output:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print("Error:", e.stderr)
        return False

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking prerequisites...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        print("❌ Python 3.7 or higher is required")
        return False
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check if required files exist
    required_files = [
        "app.py",
        "routes.py", 
        "controllers.py",
        "jira_service.py",
        "validation.py",
        "helpers.py",
        "config.py",
        "templates/index.html",
        "static/css/style.css",
        "static/js/script.js"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    dependencies = [
        "pyinstaller",
        "pywebview",
        "flask",
        "flask-cors",
        "pandas",
        "requests",
        "openpyxl"
    ]
    
    for dep in dependencies:
        print(f"Installing {dep}...")
        if not run_command(f"{sys.executable} -m pip install {dep}", f"Installing {dep}"):
            return False
    
    return True

def build_application():
    """Build the standalone application"""
    print("\n🔨 Building application...")
    
    # Run the build script
    if not run_command(f"{sys.executable} build_app.py", "Building application"):
        return False
    
    # Check if executable was created
    system = platform.system().lower()
    if system == "windows":
        exe_name = "JiraTicketManager.exe"
    else:
        exe_name = "JiraTicketManager"
    
    if not os.path.exists(exe_name):
        print(f"❌ Executable {exe_name} was not created")
        return False
    
    print(f"✅ Application built successfully: {exe_name}")
    return True

def create_distribution():
    """Create distribution packages"""
    print("\n📦 Creating distribution packages...")
    
    # Run the distribution script
    if not run_command(f"{sys.executable} create_distribution.py", "Creating distribution packages"):
        return False
    
    return True

def test_application():
    """Test the built application"""
    print("\n🧪 Testing application...")
    
    system = platform.system().lower()
    if system == "windows":
        exe_name = "JiraTicketManager.exe"
    else:
        exe_name = "JiraTicketManager"
    
    if not os.path.exists(exe_name):
        print(f"❌ Executable {exe_name} not found for testing")
        return False
    
    print(f"✅ Application {exe_name} is ready for testing")
    print("💡 To test the application:")
    print(f"   - Double-click {exe_name}")
    print("   - Or run it from the command line")
    print("   - The app should open in a desktop window")
    
    return True

def cleanup_build_files():
    """Clean up build artifacts"""
    print("\n🧹 Cleaning up build artifacts...")
    
    # Files to remove
    files_to_remove = [
        "desktop_app.py",
        "build",
        "__pycache__",
        "JiraTicketManager.spec"
    ]
    
    # Directories to remove
    dirs_to_remove = [
        "build",
        "__pycache__"
    ]
    
    import shutil
    
    for file in files_to_remove:
        if os.path.exists(file):
            if os.path.isfile(file):
                os.remove(file)
                print(f"✓ Removed {file}")
            elif os.path.isdir(file):
                shutil.rmtree(file)
                print(f"✓ Removed {file}")
    
    print("✅ Cleanup completed")

def show_final_summary():
    """Show final summary of what was created"""
    print("\n🎉 BUILD AND DISTRIBUTION COMPLETED!")
    print("=" * 50)
    
    system = platform.system().lower()
    
    print("\n📁 Generated Files:")
    
    # Check for executables
    if system == "windows":
        if os.path.exists("JiraTicketManager.exe"):
            print("  ✅ JiraTicketManager.exe (Windows executable)")
    else:
        if os.path.exists("JiraTicketManager"):
            print("  ✅ JiraTicketManager (macOS/Linux executable)")
    
    # Check for distribution packages
    distribution_files = [
        f"JiraTicketManager_{system.capitalize()}.zip",
        "JiraTicketManager_Universal.zip"
    ]
    
    for file in distribution_files:
        if os.path.exists(file):
            size = os.path.getsize(file) / (1024 * 1024)  # Size in MB
            print(f"  ✅ {file} ({size:.1f} MB)")
    
    # Check for documentation
    if os.path.exists("APP_README.md"):
        print("  ✅ APP_README.md (User documentation)")
    
    if os.path.exists("sample_tickets.xlsx"):
        print("  ✅ sample_tickets.xlsx (Sample data)")
    
    print("\n📤 Ready to Share!")
    print("\nFor Windows users:")
    print("  - Send JiraTicketManager_Windows.zip")
    
    print("\nFor macOS users:")
    print("  - Send JiraTicketManager_macOS.zip")
    
    print("\nFor Linux users:")
    print("  - Send JiraTicketManager_Linux.zip")
    
    print("\nFor all platforms:")
    print("  - Send JiraTicketManager_Universal.zip")
    
    print("\n💡 Distribution Tips:")
    print("  - Share via email, cloud storage, or file sharing")
    print("  - Include the sample Excel file for testing")
    print("  - Provide the APP_README.md for user guidance")
    print("  - Test the app on a clean system before distribution")

def main():
    """Main function"""
    print("🚀 Jira Ticket Manager - Complete Build & Distribution")
    print("=" * 60)
    print("This script will:")
    print("1. Check prerequisites")
    print("2. Install dependencies")
    print("3. Build the standalone application")
    print("4. Create distribution packages")
    print("5. Test the application")
    print("6. Clean up build artifacts")
    print("=" * 60)
    
    # Ask for confirmation
    response = input("\nDo you want to continue? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Build cancelled.")
        return
    
    start_time = time.time()
    
    # Step 1: Check prerequisites
    if not check_prerequisites():
        print("❌ Prerequisites check failed. Please fix the issues above.")
        return
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("❌ Dependency installation failed.")
        return
    
    # Step 3: Build application
    if not build_application():
        print("❌ Application build failed.")
        return
    
    # Step 4: Create distribution
    if not create_distribution():
        print("❌ Distribution creation failed.")
        return
    
    # Step 5: Test application
    test_application()
    
    # Step 6: Cleanup
    cleanup_build_files()
    
    # Show final summary
    show_final_summary()
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n⏱️  Total build time: {duration:.1f} seconds")
    print("\n🎯 Your standalone Jira Ticket Manager is ready for distribution!")

if __name__ == "__main__":
    main() 