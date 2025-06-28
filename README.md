# Jira Ticket Manager - Modular Architecture

A Flask-based application for creating Jira tickets from Excel files with a clean, modular architecture designed for scalability and maintainability.

## 🏗️ Architecture Overview

The application follows a modular design pattern with clear separation of concerns:

```
jira/
├── app.py              # Main application entry point
├── routes.py           # HTTP route handlers
├── controllers.py      # Business logic controllers
├── jira_service.py     # Jira API integration
├── validation.py       # Data validation logic
├── helpers.py          # Utility functions
├── config.py           # Configuration management
├── requirements.txt    # Python dependencies
├── static/             # Static assets (CSS, JS)
├── templates/          # HTML templates
└── uploads/            # Temporary file storage
```

## 📁 Module Documentation

### 1. `app.py` - Application Entry Point

**Purpose**: Main Flask application initialization and configuration

**Key Functions**:

- `create_app()`: Creates and configures the Flask application
- `main()`: Application entry point with server startup

**Features**:

- Environment-based configuration
- CORS support
- Automatic directory creation
- Logging configuration

### 2. `routes.py` - HTTP Route Handlers

**Purpose**: Defines all HTTP endpoints and request handling

**Key Routes**:

- `GET /`: Main application page
- `POST /api/upload`: File upload endpoint
- `POST /api/create-tickets`: Start ticket creation
- `GET /api/status/<id>`: Get operation status
- `GET /api/ticket/<key>`: Get ticket details
- `POST /api/search`: Search tickets with JQL
- `GET /api/health`: Health check endpoint

**Features**:

- Comprehensive error handling
- Request validation
- JSON response formatting
- Logging for debugging

### 3. `controllers.py` - Business Logic Controllers

**Purpose**: Orchestrates business logic and coordinates between services

**Classes**:

- `FileUploadController`: Handles file upload and processing
- `TicketCreationController`: Manages ticket creation operations
- `TicketSearchController`: Handles ticket search and retrieval

**Features**:

- Background processing with threading
- Progress tracking
- Data cleanup and management
- Operation status management

### 4. `jira_service.py` - Jira API Integration

**Purpose**: Handles all Jira API interactions

**Key Features**:

- `JiraService` class with comprehensive API methods
- Authentication handling
- Request/response management
- Error handling and retry logic
- Support for multiple Jira operations

**Methods**:

- `create_ticket()`: Create single ticket
- `create_multiple_tickets()`: Bulk ticket creation
- `get_ticket_details()`: Retrieve ticket information
- `search_tickets()`: JQL-based search
- `test_connection()`: Validate Jira connectivity

### 5. `validation.py` - Data Validation

**Purpose**: Comprehensive data validation for Excel files and ticket data

**Validation Functions**:

- `validate_excel_structure()`: Check Excel file structure
- `validate_ticket_data()`: Validate individual ticket rows
- `validate_all_tickets()`: Bulk validation
- `comprehensive_validation()`: Complete validation pipeline

**Features**:

- Required field validation
- Data type checking
- Length restrictions
- Format validation
- Security checks

### 6. `helpers.py` - Utility Functions

**Purpose**: Common utility functions used across the application

**Key Functions**:

- File operations (read, clean, convert)
- ID generation (UUID-based)
- Response formatting
- File management
- Data processing utilities

**Features**:

- Standardized error/success responses
- File size and type validation
- Data cleaning and transformation
- Memory management utilities

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Jira instance with API access
- API token for authentication

### Installation

1. **Clone and navigate to the project**:

```bash
cd jira
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Configure Jira credentials**:
   Edit `config.py` with your Jira details:

```python
JIRA_CONFIG = {
    'JIRA_BASE_URL': 'https://your-domain.atlassian.net',
    'JIRA_USERNAME': 'your-email@domain.com',
    'JIRA_API_TOKEN': 'your-api-token',
    'JIRA_PROJECT_KEY': 'PROJ'
}
```

4. **Run the application**:

```bash
python app.py
```

The application will be available at `http://localhost:4000`

## 📊 Excel File Format

Your Excel file should contain the following columns:

| Column        | Required | Description            | Example                  |
| ------------- | -------- | ---------------------- | ------------------------ |
| `summary`     | Yes      | Ticket summary/title   | "Fix login bug"          |
| `description` | Yes      | Detailed description   | "Users cannot log in..." |
| `issue_type`  | Yes      | Type of issue          | "bug", "task", "story"   |
| `priority`    | Yes      | Priority level         | "high", "medium", "low"  |
| `project_key` | No       | Jira project key       | "PROJ"                   |
| `assignee`    | No       | Username to assign     | "john.doe"               |
| `labels`      | No       | Comma-separated labels | "frontend,urgent"        |

## 🔧 Configuration

### Environment Variables

- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 4000)
- `DEBUG`: Debug mode (default: False)
- `SECRET_KEY`: Flask secret key

### Jira Configuration

All Jira settings are managed in `config.py`:

- Base URL
- Username/Email
- API Token
- Default Project Key

## 🛠️ Development

### Adding New Features

1. **New API Endpoint**:

   - Add route in `routes.py`
   - Implement business logic in appropriate controller
   - Add validation if needed

2. **New Validation Rule**:

   - Add function in `validation.py`
   - Update `comprehensive_validation()` if needed

3. **New Jira Operation**:
   - Add method to `JiraService` class
   - Implement in `jira_service.py`

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to all functions
- Use type hints
- Include error handling
- Add logging for debugging

### Testing

```bash
# Run with debug mode
DEBUG=true python app.py

# Check health endpoint
curl http://localhost:4000/api/health
```

## 🔍 Troubleshooting

### Common Issues

1. **Jira Connection Failed**:

   - Verify API token is correct
   - Check base URL format
   - Ensure user has appropriate permissions

2. **File Upload Issues**:

   - Check file format (Excel only)
   - Verify required columns exist
   - Check file size limits

3. **Ticket Creation Errors**:
   - Validate Excel data format
   - Check Jira project permissions
   - Verify issue types and priorities

### Debug Mode

Enable debug mode for detailed logging:

```bash
DEBUG=true python app.py
```

## 📈 Scaling Considerations

### Performance

- Background processing for large files
- Automatic cleanup of old data
- Memory-efficient data handling
- Rate limiting for Jira API calls

### Production Deployment

- Use production WSGI server (Gunicorn)
- Implement proper logging
- Add monitoring and health checks
- Use environment variables for secrets
- Consider database for data persistence

### Security

- Input validation and sanitization
- File upload restrictions
- API token security
- CORS configuration
- Error message sanitization

## 🤝 Contributing

1. Follow the modular architecture
2. Add comprehensive documentation
3. Include error handling
4. Add logging for debugging
5. Test thoroughly before submitting

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
