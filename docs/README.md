# Jira Ticket Manager - Documentation

This folder contains comprehensive documentation for the Jira Ticket Manager system architecture and implementation.

## 📚 Documentation Index

### 🏗️ System Architecture

- **[SYSTEM_ARCHITECTURE.md](./SYSTEM_ARCHITECTURE.md)** - Complete system architecture overview with high-level design diagrams, component responsibilities, and scalability considerations.

### 🔄 API Documentation

- **[API_MAPPING.md](./API_MAPPING.md)** - Detailed API endpoint mapping, request flow diagrams, and controller-service relationships.

## 🚀 Quick Start

1. **Read the System Architecture** to understand the overall design
2. **Review API Mapping** to understand how requests flow through the system
3. **Check the main README.md** in the project root for setup and usage instructions

## 📋 Documentation Structure

```
docs/
├── README.md                    # This file - Documentation index
├── SYSTEM_ARCHITECTURE.md       # High-level system design
└── API_MAPPING.md              # API endpoints and flow diagrams
```

## 🎯 Key Architecture Components

### Controllers

- **FileUploadController**: Handles file upload and preview generation
- **TicketCreationController**: Manages ticket creation and status tracking
- **TicketSearchController**: Handles ticket retrieval and search

### Services

- **JiraService**: All Jira API interactions
- **Validation**: Data validation and security checks
- **Helpers**: Utility functions and file operations

### API Endpoints

- `/api/upload` - File upload and parsing
- `/api/create-tickets` - Start ticket creation
- `/api/status/<id>` - Check operation status
- `/api/ticket/<key>` - Get ticket details
- `/api/search` - Search tickets with JQL

## 🔧 Development Workflow

1. **Understanding the System**: Start with SYSTEM_ARCHITECTURE.md
2. **API Development**: Reference API_MAPPING.md for endpoint design
3. **Implementation**: Follow the modular structure outlined in the architecture
4. **Testing**: Use the test_modular.py script to verify functionality

## 📈 Future Documentation

Planned documentation additions:

- Database schema design (when implemented)
- Deployment guides
- API reference documentation
- Troubleshooting guides
- Performance optimization guides

---

For questions or contributions to the documentation, please refer to the main project README.md in the root directory.
