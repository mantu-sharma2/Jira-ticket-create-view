# Jira Ticket Manager - Desktop Application

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
