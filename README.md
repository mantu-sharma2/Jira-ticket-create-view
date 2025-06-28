# Jira Ticket Manager

A modern, clean Flask-based web application for bulk Jira ticket creation from Excel files and viewing ticket details.

## Features

- **Bulk Ticket Creation**: Upload Excel files to create multiple Jira tickets
- **Real-time Progress**: Live status updates during ticket creation
- **Data Preview**: Review Excel data before creating tickets
- **Ticket Viewer**: Search and view existing Jira tickets
- **Modern UI**: Clean, responsive design with intuitive navigation
- **Error Handling**: Comprehensive error handling and user feedback

## Prerequisites

- Python 3.8 or higher
- Jira instance with API access
- Jira API token

## Installation

1. **Clone or download the project**

   ```bash
   git clone <repository-url>
   cd jira-ticket-manager
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Jira credentials**

   Create a `.env` file in the project root:

   ```env
   JIRA_BASE_URL=https://your-domain.atlassian.net
   JIRA_API_TOKEN=your-api-token-here
   JIRA_EMAIL=your-email@domain.com
   DEFAULT_PROJECT_KEY=PROJ
   ```

   **How to get Jira API token:**

   1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
   2. Click "Create API token"
   3. Give it a name and copy the token

## Usage

### Running the Application

1. **Start the Flask server**

   ```bash
   python app.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:4000`

### Creating Tickets from Excel

1. **Prepare your Excel file** with the following columns:

   - **Required**: `summary`, `description`, `issue_type`, `priority`
   - **Optional**: `project_key`, `assignee`, `labels`

2. **Upload the file**:

   - Click "Choose File" or drag and drop
   - Review the data preview
   - Click "Create Tickets"

3. **Monitor progress**:
   - Real-time status updates for each ticket
   - Success/failure indicators
   - Final summary report

### Viewing Tickets

1. **Switch to "View Ticket Details" tab**
2. **Enter a ticket ID** (e.g., PROJ-123)
3. **View comprehensive ticket information**:
   - Summary and description
   - Issue type and priority
   - Assignee and status
   - Creation date and labels
   - Direct link to Jira

## Excel File Format

### Required Columns

| Column        | Description          | Example                                      |
| ------------- | -------------------- | -------------------------------------------- |
| `summary`     | Ticket title/summary | "Fix login bug"                              |
| `description` | Detailed description | "Users cannot log in with valid credentials" |
| `issue_type`  | Type of issue        | "Bug", "Task", "Story"                       |
| `priority`    | Priority level       | "High", "Medium", "Low"                      |

### Optional Columns

| Column        | Description            | Example               |
| ------------- | ---------------------- | --------------------- |
| `project_key` | Jira project key       | "PROJ"                |
| `assignee`    | Username of assignee   | "john.doe"            |
| `labels`      | Comma-separated labels | "bug,frontend,urgent" |

### Sample Excel File

| summary              | description                                | issue_type | priority | assignee   | labels       |
| -------------------- | ------------------------------------------ | ---------- | -------- | ---------- | ------------ |
| Fix login bug        | Users cannot log in with valid credentials | Bug        | High     | john.doe   | bug,frontend |
| Update documentation | Update API documentation                   | Task       | Medium   | jane.smith | docs,api     |

## Configuration

### Environment Variables

| Variable              | Description            | Default        |
| --------------------- | ---------------------- | -------------- |
| `JIRA_BASE_URL`       | Your Jira instance URL | Required       |
| `JIRA_API_TOKEN`      | Your Jira API token    | Required       |
| `JIRA_EMAIL`          | Your Jira email        | Required       |
| `DEFAULT_PROJECT_KEY` | Default project key    | "PROJ"         |
| `SECRET_KEY`          | Flask secret key       | Auto-generated |

### Jira Configuration

The application supports:

- **Jira Cloud** (atlassian.net)
- **Jira Server** (self-hosted)
- **Custom field mapping**
- **Multiple project support**

## Development

### Project Structure

```
jira-ticket-manager/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .env                  # Environment variables (create this)
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Stylesheets
│   └── js/
│       └── script.js     # JavaScript functionality
└── uploads/              # Temporary file storage
```

### Key Components

- **Flask Backend**: RESTful API endpoints
- **Frontend**: Modern JavaScript with ES6 classes
- **Data Processing**: Pandas for Excel handling
- **Jira Integration**: REST API client
- **Real-time Updates**: WebSocket-like polling

### API Endpoints

| Endpoint          | Method | Description                 |
| ----------------- | ------ | --------------------------- |
| `/`               | GET    | Main application page       |
| `/upload`         | POST   | Upload and parse Excel file |
| `/preview/<id>`   | GET    | Get preview data            |
| `/create-tickets` | POST   | Start ticket creation       |
| `/status/<id>`    | GET    | Get operation status        |
| `/ticket/<id>`    | GET    | Get ticket details          |

## Troubleshooting

### Common Issues

1. **Port 4000 already in use**

   ```bash
   # Find and kill the process
   lsof -ti:4000 | xargs kill -9
   ```

2. **Jira authentication errors**

   - Verify API token is correct
   - Check email address
   - Ensure proper permissions

3. **Excel parsing errors**

   - Verify required columns exist
   - Check for empty required fields
   - Ensure file format is .xlsx or .xls

4. **File upload not working**
   - Check browser console for errors
   - Verify file size (max 10MB)
   - Ensure proper file format

### Debug Mode

Enable debug logging:

```python
# In app.py, change:
app.run(debug=True, host='0.0.0.0', port=4000)
```

### Browser Console

Open browser developer tools (F12) to see:

- JavaScript errors
- Network requests
- Console logs

## Security Considerations

- **API Tokens**: Store securely, never commit to version control
- **File Uploads**: Validate file types and sizes
- **CORS**: Configure appropriately for production
- **HTTPS**: Use in production environments

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:4000 app:app
```

### Using Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 4000
CMD ["python", "app.py"]
```

### Environment Setup

```bash
# Production environment variables
export FLASK_ENV=production
export SECRET_KEY=your-secure-secret-key
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review browser console logs
3. Check Flask application logs
4. Create an issue with detailed information

## Changelog

### Version 1.0.0

- Initial release
- Bulk ticket creation from Excel
- Real-time progress tracking
- Ticket viewing functionality
- Modern responsive UI
