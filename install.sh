#!/bin/bash
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
