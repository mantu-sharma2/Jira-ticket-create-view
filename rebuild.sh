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