# Jira Ticket Manager - System Architecture (HLD)

## 🏗️ System Overview

The Jira Ticket Manager is a Flask-based web application with a modular architecture designed for scalability, maintainability, and clear separation of concerns.

## 📊 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐            │
│  │   Web Browser   │    │   Mobile App    │    │   API Client    │            │
│  │   (Frontend)    │    │   (Future)      │    │   (Future)      │            │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘            │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP/HTTPS
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PRESENTATION LAYER                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              FLASK APP                                      │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │ │
│  │  │   Templates     │  │   Static Files  │  │   Error Handler │            │ │
│  │  │   (HTML/CSS)    │  │   (JS/CSS/IMG)  │  │   (404/500)     │            │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘            │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Route Registration
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              ROUTING LAYER                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              ROUTES.PY                                      │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │ │
│  │  │ GET /       │  │POST /api/   │  │POST /api/   │  │GET /api/    │      │ │
│  │  │ (Index)     │  │upload       │  │create-      │  │status/<id>  │      │ │
│  │  │             │  │             │  │tickets      │  │             │      │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │ │
│  │  │GET /api/    │  │POST /api/   │  │GET /api/    │  │POST /api/   │      │ │
│  │  │ticket/<key> │  │search       │  │health       │  │cleanup      │      │ │
│  │  │             │  │             │  │             │  │             │      │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Controller Calls
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CONTROLLER LAYER                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           CONTROLLERS.PY                                   │ │
│  │                                                                             │ │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │                FileUploadController                                     │ │ │
│  │  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │ │ │
│  │  │  │process_file_    │  │get_preview_     │  │_cleanup_old_    │        │ │ │
│  │  │  │upload()         │  │data()           │  │previews()       │        │ │ │
│  │  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │ │ │
│  │  └─────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                             │ │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │              TicketCreationController                                   │ │ │
│  │  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │ │ │
│  │  │  │start_ticket_    │  │get_operation_   │  │cleanup_old_     │        │ │ │
│  │  │  │creation()       │  │status()         │  │operations()     │        │ │ │
│  │  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │ │ │
│  │  └─────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                             │ │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │                TicketSearchController                                   │ │ │
│  │  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │ │ │
│  │  │  │get_ticket_      │  │search_tickets() │  │_is_valid_       │        │ │ │
│  │  │  │details()        │  │                 │  │ticket_key()     │        │ │ │
│  │  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │ │ │
│  │  └─────────────────────────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Service Calls
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SERVICE LAYER                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           JIRA_SERVICE.PY                                  │ │
│  │                                                                             │ │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │                        JiraService Class                                │ │ │
│  │  │                                                                         │ │ │
│  │  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │ │ │ │
│  │  │  │create_ticket()  │  │create_multiple_ │  │get_ticket_      │        │ │ │ │
│  │  │  │                 │  │tickets()        │  │details()        │        │ │ │ │
│  │  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │ │ │ │
│  │  │                                                                         │ │ │ │
│  │  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │ │ │ │
│  │  │  │search_tickets() │  │test_connection()│  │get_project_     │        │ │ │ │
│  │  │  │                 │  │                 │  │info()           │        │ │ │ │
│  │  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │ │ │ │
│  │  │                                                                         │ │ │ │
│  │  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │ │ │ │
│  │  │  │update_ticket()  │  │delete_ticket()  │  │_prepare_ticket_ │        │ │ │ │
│  │  │  │                 │  │                 │  │payload()        │        │ │ │ │
│  │  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │ │ │ │
│  │  └─────────────────────────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Validation & Helper Calls
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              UTILITY LAYER                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           VALIDATION.PY                                    │ │
│  │                                                                             │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │ │
│  │  │validate_excel_  │  │validate_ticket_ │  │validate_all_    │            │ │
│  │  │structure()      │  │data()           │  │tickets()        │            │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘            │ │
│  │                                                                             │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │ │
│  │  │validate_file_   │  │validate_        │  │comprehensive_   │            │ │
│  │  │size()           │  │filename()       │  │validation()     │            │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘            │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                            HELPERS.PY                                       │ │
│  │                                                                             │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │ │
│  │  │read_excel_file()│  │clean_dataframe()│  │convert_df_to_   │            │ │
│  │  │                 │  │                 │  │dict()           │            │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘            │ │
│  │                                                                             │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │ │
│  │  │generate_preview_│  │create_success_  │  │create_error_    │            │ │
│  │  │id()             │  │response()       │  │response()       │            │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘            │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ External API Calls
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              EXTERNAL LAYER                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              JIRA API                                       │ │
│  │                                                                             │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │ │
│  │  │   REST API      │  │   Authentication│  │   Rate Limiting │            │ │
│  │  │   Endpoints     │  │   (Basic Auth)  │  │   & Quotas      │            │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘            │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 API Endpoint Mapping

### File Upload Flow

```
Client → /api/upload → FileUploadController → Validation → Helpers → JiraService
```

### Ticket Creation Flow

```
Client → /api/create-tickets → TicketCreationController → JiraService → Background Thread
```

### Status Check Flow

```
Client → /api/status/<id> → TicketCreationController → In-Memory Store
```

### Ticket Search Flow

```
Client → /api/ticket/<key> → TicketSearchController → JiraService → Jira API
```

## 📋 Component Responsibilities

### 🎯 **Controllers** (`controllers.py`)

- **FileUploadController**: Handles file upload, parsing, and preview generation
- **TicketCreationController**: Manages ticket creation operations and status tracking
- **TicketSearchController**: Handles ticket retrieval and search operations

### 🔧 **Services** (`jira_service.py`)

- **JiraService**: All Jira API interactions, authentication, and data transformation
- **HTTP Client**: Request/response handling with error management
- **Data Mapping**: Converts between internal format and Jira API format

### ✅ **Validation** (`validation.py`)

- **Excel Structure**: Validates file format and required columns
- **Ticket Data**: Validates individual ticket fields and business rules
- **Security**: File type, size, and content validation

### 🛠️ **Helpers** (`helpers.py`)

- **File Operations**: Excel reading, cleaning, and conversion
- **ID Generation**: UUID-based unique identifiers
- **Response Formatting**: Standardized success/error responses
- **Utilities**: Common functions used across the application

### 🛣️ **Routes** (`routes.py`)

- **HTTP Endpoints**: All API route definitions
- **Request Handling**: Input validation and error handling
- **Response Formatting**: JSON response structure

## 🔐 Data Flow Security

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │───▶│   Routes    │───▶│ Controllers │───▶│  Services   │
│             │    │             │    │             │    │             │
│  (Browser)  │    │ Validation  │    │ Validation  │    │ Validation  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Input     │    │   Request   │    │   Business  │    │   External  │
│ Validation  │    │   Sanitize  │    │   Logic     │    │   API Call  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## 📊 State Management

### In-Memory Storage

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              GLOBAL STORES                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  preview_data_store = {                                                    │
│    'preview_id': {                                                         │
│      'file_path': str,                                                     │
│      'data': List[Dict],                                                   │
│      'columns': List[str],                                                 │
│      'created_at': datetime                                                │
│    }                                                                        │
│  }                                                                          │
│                                                                             │
│  operation_status_store = {                                                │
│    'operation_id': {                                                       │
│      'status': str,                                                        │
│      'total_tickets': int,                                                 │
│      'completed': int,                                                     │
│      'failed': int,                                                        │
│      'tickets': List[Dict],                                                │
│      'errors': List[Dict]                                                  │
│    }                                                                        │
│  }                                                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 Background Processing

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Controller    │───▶│  Background     │───▶│   Jira API      │
│                 │    │   Thread        │    │                 │
│ Start Operation │    │ Process Tickets │    │ Create Tickets  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
       │                        │                        │
       ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Return Operation│    │ Update Status   │    │ Return Results  │
│      ID         │    │   Store         │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Scalability Considerations

### Horizontal Scaling

- **Stateless Design**: Controllers and services are stateless
- **Session Management**: No server-side session dependencies
- **Load Balancing**: Multiple instances can handle requests

### Performance Optimization

- **Background Processing**: Long-running operations don't block requests
- **Memory Management**: Automatic cleanup of old data
- **Rate Limiting**: Built-in delays to respect Jira API limits

### Future Enhancements

- **Database Integration**: Replace in-memory stores with persistent storage
- **Message Queue**: Use Redis/RabbitMQ for background job processing
- **Caching**: Implement Redis caching for frequently accessed data
- **Microservices**: Split into separate services for different domains

## 🔧 Configuration Management

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CONFIG.PY                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  JIRA_CONFIG = {                                                            │
│    'JIRA_BASE_URL': 'https://your-domain.atlassian.net',                   │
│    'JIRA_USERNAME': 'your-email@domain.com',                               │
│    'JIRA_API_TOKEN': 'your-api-token-here',                                │
│    'JIRA_PROJECT_KEY': 'PROJ'                                              │
│  }                                                                          │
│                                                                             │
│  Environment Variables:                                                     │
│  - HOST: Server host (default: 0.0.0.0)                                    │
│  - PORT: Server port (default: 4000)                                       │
│  - DEBUG: Debug mode (default: False)                                      │
│  - SECRET_KEY: Flask secret key                                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

This architecture provides a clean, maintainable, and scalable foundation for the Jira Ticket Manager application.
