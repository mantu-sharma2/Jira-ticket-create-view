# Jira Ticket Manager - API Mapping & Request Flow

## 🔄 Complete API Endpoint Mapping

### 📊 API Endpoint Overview

| HTTP Method | Endpoint               | Controller               | Service     | Description                 |
| ----------- | ---------------------- | ------------------------ | ----------- | --------------------------- |
| `GET`       | `/`                    | Routes                   | -           | Main application page       |
| `POST`      | `/api/upload`          | FileUploadController     | -           | Upload and parse Excel file |
| `POST`      | `/api/create-tickets`  | TicketCreationController | JiraService | Start ticket creation       |
| `GET`       | `/api/status/<id>`     | TicketCreationController | -           | Get operation status        |
| `GET`       | `/api/ticket/<key>`    | TicketSearchController   | JiraService | Get ticket details          |
| `POST`      | `/api/search`          | TicketSearchController   | JiraService | Search tickets with JQL     |
| `GET`       | `/api/health`          | Routes                   | JiraService | Health check                |
| `GET`       | `/api/config/validate` | Routes                   | JiraService | Validate configuration      |
| `POST`      | `/api/cleanup`         | Routes                   | -           | Clean up old data           |

## 🏗️ Detailed Request Flow Diagrams

### 1. File Upload Flow (`POST /api/upload`)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │───▶│   Routes    │───▶│FileUpload   │───▶│ Validation  │
│             │    │             │    │Controller   │    │             │
│ Upload File │    │ /api/upload │    │process_file_│    │validate_    │
│             │    │             │    │upload()     │    │filename()   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                              │
                                                              ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Helpers   │◀───│ Validation  │◀───│FileUpload   │◀───│ Validation  │
│             │    │             │    │Controller   │    │             │
│read_excel_  │    │validate_    │    │             │    │validate_    │
│file()       │    │excel_       │    │             │    │file_size()  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│clean_data-  │    │comprehensive│    │Store Preview│    │Return       │
│frame()      │    │_validation()│    │Data         │    │Response     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

**Services Used:**

- **Routes**: Request handling and response formatting
- **FileUploadController**: Business logic for file processing
- **Validation**: File and data validation
- **Helpers**: File operations and data cleaning

### 2. Ticket Creation Flow (`POST /api/create-tickets`)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │───▶│   Routes    │───▶│TicketCreation│───▶│FileUpload   │
│             │    │             │    │Controller   │    │Controller   │
│Create       │    │/api/create- │    │start_ticket_│    │get_preview_ │
│Tickets      │    │tickets      │    │creation()   │    │data()       │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                              │
                                                              ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   JiraService│◀───│TicketCreation│◀───│TicketCreation│◀───│FileUpload   │
│             │    │Controller   │    │Controller   │    │Controller   │
│validate_    │    │             │    │             │    │             │
│jira_config()│    │             │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│Background   │    │Store        │    │Return       │    │Start        │
│Thread       │    │Operation    │    │Operation ID │    │Status Check │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

**Services Used:**

- **Routes**: Request handling
- **TicketCreationController**: Business logic for ticket creation
- **FileUploadController**: Retrieve preview data
- **JiraService**: Validate configuration and create tickets

### 3. Status Check Flow (`GET /api/status/<id>`)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │───▶│   Routes    │───▶│TicketCreation│───▶│In-Memory    │
│             │    │             │    │Controller   │    │Store        │
│Check Status │    │/api/status/ │    │get_operation│    │operation_   │
│             │    │<id>         │    │_status()    │    │status_store │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                              │
                                                              ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │◀───│   Routes    │◀───│TicketCreation│◀───│In-Memory    │
│             │    │             │    │Controller   │    │Store        │
│Display      │    │Return JSON  │    │Return       │    │Return       │
│Progress     │    │Response     │    │Status Data  │    │Status Data  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

**Services Used:**

- **Routes**: Request handling and response formatting
- **TicketCreationController**: Retrieve operation status
- **In-Memory Store**: Status data storage

### 4. Ticket Search Flow (`GET /api/ticket/<key>`)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │───▶│   Routes    │───▶│TicketSearch │───▶│TicketSearch │
│             │    │             │    │Controller   │    │Controller   │
│Search       │    │/api/ticket/ │    │get_ticket_  │    │_is_valid_   │
│Ticket       │    │<key>        │    │details()    │    │ticket_key() │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                              │
                                                              ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │◀───│   Routes    │◀───│TicketSearch │◀───│JiraService  │
│             │    │             │    │Controller   │    │             │
│Display      │    │Return JSON  │    │Return       │    │get_ticket_  │
│Ticket       │    │Response     │    │Ticket Data  │    │details()    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

**Services Used:**

- **Routes**: Request handling and response formatting
- **TicketSearchController**: Business logic and validation
- **JiraService**: Jira API interaction

### 5. Ticket Search with JQL Flow (`POST /api/search`)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │───▶│   Routes    │───▶│TicketSearch │───▶│TicketSearch │
│             │    │             │    │Controller   │    │Controller   │
│Search with  │    │/api/search  │    │search_      │    │Validate JQL │
│JQL          │    │             │    │tickets()    │    │Query        │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                              │
                                                              ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │◀───│   Routes    │◀───│TicketSearch │◀───│JiraService  │
│             │    │             │    │Controller   │    │             │
│Display      │    │Return JSON  │    │Return       │    │search_      │
│Results      │    │Response     │    │Search Data  │    │tickets()    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

**Services Used:**

- **Routes**: Request handling and response formatting
- **TicketSearchController**: Business logic and JQL validation
- **JiraService**: Jira API search interaction

## 🎯 Controller Responsibilities Matrix

| Controller                   | Primary Responsibilities                 | API Endpoints                             | Services Used                     |
| ---------------------------- | ---------------------------------------- | ----------------------------------------- | --------------------------------- |
| **FileUploadController**     | File upload, parsing, preview generation | `/api/upload`                             | Validation, Helpers               |
| **TicketCreationController** | Ticket creation, status tracking         | `/api/create-tickets`, `/api/status/<id>` | JiraService, FileUploadController |
| **TicketSearchController**   | Ticket retrieval, search operations      | `/api/ticket/<key>`, `/api/search`        | JiraService                       |
| **Routes**                   | HTTP handling, error management          | All endpoints                             | All Controllers                   |

## 🔧 Service Dependencies

### JiraService Dependencies

```
JiraService
├── config.py (JIRA_CONFIG)
├── requests (HTTP client)
├── base64 (authentication)
└── logging (error tracking)
```

### Validation Dependencies

```
Validation
├── helpers.py (validate_file_extension)
├── pandas (DataFrame validation)
├── re (regex validation)
└── logging (validation errors)
```

### Helpers Dependencies

```
Helpers
├── pandas (Excel operations)
├── uuid (ID generation)
├── datetime (timestamps)
├── os (file operations)
└── logging (debugging)
```

## 📊 Data Flow Patterns

### 1. Request-Response Pattern

```
Client Request → Routes → Controller → Service → External API → Response
```

### 2. Background Processing Pattern

```
Client Request → Controller → Background Thread → Service → Status Update
```

### 3. Validation Pattern

```
Input Data → Validation → Controller → Service → Response
```

### 4. Error Handling Pattern

```
Error → Service → Controller → Routes → Client (with error details)
```

## 🔄 Background Processing Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Controller    │───▶│  Background     │───▶│   JiraService   │
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

## 🛡️ Security & Validation Layers

### Input Validation

1. **Routes Layer**: Basic request validation
2. **Controller Layer**: Business logic validation
3. **Service Layer**: API-specific validation
4. **External Layer**: Jira API validation

### Error Handling

1. **Service Layer**: API errors and timeouts
2. **Controller Layer**: Business logic errors
3. **Routes Layer**: HTTP errors and exceptions
4. **Client Layer**: User-friendly error display

This comprehensive API mapping provides a clear understanding of how requests flow through the system and which components are responsible for each part of the process.
