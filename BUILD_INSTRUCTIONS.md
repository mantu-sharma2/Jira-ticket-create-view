# Jira Ticket Manager - Build Instructions

This guide provides step-by-step instructions for rebuilding the Jira Ticket Manager application whenever you make changes to the code.

## 🎯 Quick Build Commands

### One-Command Build (Recommended)

```bash
# Set PATH and build in one command
export PATH=$PATH:/Users/darkshadow/Library/Python/3.9/bin && python3 build_and_distribute.py
```

### Manual Build Commands

```bash
# 1. Set PATH for PyInstaller
export PATH=$PATH:/Users/darkshadow/Library/Python/3.9/bin

# 2. Clean previous builds
rm -rf dist/ build/ __pycache__/ && rm -f JiraTicketManager.spec

# 3. Build the executable
pyinstaller --onefile --name=JiraTicketManager --add-data=templates:templates --add-data=static:static --add-data=config.py:config.py --hidden-import=flask --hidden-import=flask_cors --hidden-import=pandas --hidden-import=requests --hidden-import=webview --hidden-import=threading --hidden-import=webbrowser --hidden-import=app --hidden-import=routes --hidden-import=controllers --hidden-import=jira_service --hidden-import=validation --hidden-import=helpers --hidden-import=config app.py

# 4. Create distribution package
mkdir -p JiraTicketManager_macOS && cp dist/JiraTicketManager JiraTicketManager_macOS/ && cp APP_README.md JiraTicketManager_macOS/ 2>/dev/null || echo "APP_README.md not found" && cp sample_tickets.xlsx JiraTicketManager_macOS/ 2>/dev/null || echo "sample_tickets.xlsx not found"

# 5. Create ZIP for distribution (optional)
zip -r JiraTicketManager_macOS.zip JiraTicketManager_macOS/
```

## 📋 Detailed Step-by-Step Process

### Step 1: Prepare Environment

```bash
# Navigate to project directory
cd /Users/darkshadow/Desktop/jira

# Set PATH for PyInstaller (if not already set)
export PATH=$PATH:/Users/darkshadow/Library/Python/3.9/bin

# Verify PyInstaller is available
pyinstaller --version
```

### Step 2: Clean Previous Builds

```bash
# Remove all build artifacts
rm -rf dist/ build/ __pycache__/
rm -f JiraTicketManager.spec
rm -f desktop_app.py
```

### Step 3: Verify Dependencies

```bash
# Check if all required packages are installed
python3 -c "import flask, flask_cors, pandas, requests, webview, webbrowser; print('All dependencies OK')"
```

### Step 4: Build the Executable

```bash
# Build with PyInstaller
pyinstaller --onefile \
  --name=JiraTicketManager \
  --add-data=templates:templates \
  --add-data=static:static \
  --add-data=config.py:config.py \
  --hidden-import=flask \
  --hidden-import=flask_cors \
  --hidden-import=pandas \
  --hidden-import=requests \
  --hidden-import=webview \
  --hidden-import=threading \
  --hidden-import=webbrowser \
  --hidden-import=app \
  --hidden-import=routes \
  --hidden-import=controllers \
  --hidden-import=jira_service \
  --hidden-import=validation \
  --hidden-import=helpers \
  --hidden-import=config \
  app.py
```

### Step 5: Test the Build

```bash
# Check if executable was created
ls -la dist/JiraTicketManager

# Test the executable (optional - will open browser)
./dist/JiraTicketManager
```

### Step 6: Create Distribution Package

```bash
# Create distribution directory
mkdir -p JiraTicketManager_macOS

# Copy executable
cp dist/JiraTicketManager JiraTicketManager_macOS/

# Copy documentation (if exists)
cp APP_README.md JiraTicketManager_macOS/ 2>/dev/null || echo "APP_README.md not found"
cp sample_tickets.xlsx JiraTicketManager_macOS/ 2>/dev/null || echo "sample_tickets.xlsx not found"

# Create README for distribution
cat > JiraTicketManager_macOS/README.md << 'EOF'
# Jira Ticket Manager - macOS

## 🚀 Quick Start

1. **Double-click** `JiraTicketManager` to run the application
2. **Chrome will automatically open** with the application
3. **Configure** your Jira credentials when prompted
4. **Start creating** tickets from Excel files!

## 📋 What This App Does

- Upload Excel files with ticket data
- Create Jira tickets automatically
- View existing ticket details
- Real-time progress tracking
- **Automatically opens in your default browser**

## 🔧 Requirements

- macOS system
- Internet connection for Jira API
- Excel files with required columns:
  - `summary` (required): Ticket title
  - `description` (required): Detailed description
  - `issue_type` (required): Type of issue (bug, task, story, etc.)
  - `priority` (required): Priority level (high, medium, low, etc.)
  - `project_key` (optional): Jira project key
  - `assignee` (optional): Username to assign the ticket to
  - `labels` (optional): Comma-separated labels

## 🎯 How It Works

1. **Start the app** - Double-click `JiraTicketManager`
2. **Browser opens automatically** - Chrome/Safari will open with the app
3. **Upload Excel file** - Use the file upload feature
4. **Review data** - Check the preview of your ticket data
5. **Create tickets** - Click "Create Tickets" to start the process
6. **Monitor progress** - Watch real-time updates as tickets are created

## 🔒 Security Notes

- The application stores your Jira credentials locally
- Keep your API tokens secure and don't share them
- The application only connects to your specified Jira instance

## 📞 Support

If you encounter any issues:
1. Make sure you have a stable internet connection
2. Verify your Jira credentials are correct
3. Check that your Excel file has the required columns
4. Ensure your Jira instance is accessible

## 🎉 Ready to Use!

Your Jira Ticket Manager is now ready to help you create tickets efficiently!

---
*Jira Ticket Manager v1.0 - Built with Python and Flask*
EOF
```

### Step 7: Create ZIP for Distribution (Optional)

```bash
# Create ZIP file for easy sharing
zip -r JiraTicketManager_macOS.zip JiraTicketManager_macOS/

# Verify ZIP was created
ls -la JiraTicketManager_macOS.zip
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. PyInstaller Not Found

```bash
# Solution: Set PATH correctly
export PATH=$PATH:/Users/darkshadow/Library/Python/3.9/bin
pyinstaller --version
```

#### 2. Build Fails with Import Errors

```bash
# Solution: Add missing hidden imports
# Add --hidden-import=missing_module to the PyInstaller command
```

#### 3. Executable Won't Start

```bash
# Solution: Check for missing dependencies
# Run: ./dist/JiraTicketManager
# Look for error messages and add missing --hidden-import flags
```

#### 4. Browser Doesn't Open

```bash
# Solution: Check webbrowser import
# Ensure --hidden-import=webbrowser is included in PyInstaller command
```

#### 5. Large Executable Size

```bash
# Solution: Exclude unnecessary modules
# Add --exclude-module=unnecessary_module to reduce size
```

## 📁 File Structure After Build

```
jira/
├── dist/
│   └── JiraTicketManager          # Main executable
├── build/                         # Build artifacts (can be deleted)
├── JiraTicketManager_macOS/       # Distribution package
│   ├── JiraTicketManager          # Executable for distribution
│   ├── README.md                  # User instructions
│   ├── APP_README.md              # Detailed documentation (if exists)
│   └── sample_tickets.xlsx        # Sample data (if exists)
├── JiraTicketManager_macOS.zip    # ZIP for distribution
└── JiraTicketManager.spec         # PyInstaller spec file
```

## 🚀 Quick Script for Future Builds

Create a file called `rebuild.sh`:

```bash
#!/bin/bash
# Quick rebuild script for Jira Ticket Manager

echo "🚀 Rebuilding Jira Ticket Manager..."

# Set PATH
export PATH=$PATH:/Users/darkshadow/Library/Python/3.9/bin

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ __pycache__/
rm -f JiraTicketManager.spec

# Build executable
echo "🔨 Building executable..."
pyinstaller --onefile \
  --name=JiraTicketManager \
  --add-data=templates:templates \
  --add-data=static:static \
  --add-data=config.py:config.py \
  --hidden-import=flask \
  --hidden-import=flask_cors \
  --hidden-import=pandas \
  --hidden-import=requests \
  --hidden-import=webview \
  --hidden-import=threading \
  --hidden-import=webbrowser \
  --hidden-import=app \
  --hidden-import=routes \
  --hidden-import=controllers \
  --hidden-import=jira_service \
  --hidden-import=validation \
  --hidden-import=helpers \
  --hidden-import=config \
  app.py

# Create distribution
echo "📦 Creating distribution package..."
mkdir -p JiraTicketManager_macOS
cp dist/JiraTicketManager JiraTicketManager_macOS/
cp APP_README.md JiraTicketManager_macOS/ 2>/dev/null || echo "APP_README.md not found"
cp sample_tickets.xlsx JiraTicketManager_macOS/ 2>/dev/null || echo "sample_tickets.xlsx not found"

# Create ZIP
echo "📦 Creating ZIP file..."
zip -r JiraTicketManager_macOS.zip JiraTicketManager_macOS/

echo "✅ Build completed successfully!"
echo "📁 Files created:"
echo "  - dist/JiraTicketManager (executable)"
echo "  - JiraTicketManager_macOS/ (distribution folder)"
echo "  - JiraTicketManager_macOS.zip (ZIP for sharing)"
```

Make it executable:

```bash
chmod +x rebuild.sh
```

Then use it:

```bash
./rebuild.sh
```

## 📝 Notes

- **Always test** the executable after building
- **Keep backups** of working versions
- **Document changes** in version notes
- **Test on clean systems** before distribution
- **Update README** if you change functionality

## 🎯 Summary

For quick rebuilds, just run:

```bash
export PATH=$PATH:/Users/darkshadow/Library/Python/3.9/bin && python3 build_and_distribute.py
```

Or use the manual commands above for more control over the build process.

---

_Last updated: June 29, 2024_
