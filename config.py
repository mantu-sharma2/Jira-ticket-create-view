# Jira Configuration
# Update these values with your actual Jira credentials

JIRA_CONFIG = {
    # Your Jira instance URL (e.g., https://yourcompany.atlassian.net)
    'JIRA_BASE_URL': 'https://your-domain.atlassian.net',
    
    # Your Jira account email address
    'JIRA_USERNAME': 'your-email@domain.com',
    
    # Your Jira API token (generate at https://id.atlassian.com/manage-profile/security/api-tokens)
    'JIRA_API_TOKEN': 'your-api-token-here',
    
    # Default project key (used if not specified in Excel file)
    'JIRA_PROJECT_KEY': 'PROJ'
}

# Legacy configuration (for backward compatibility)
JIRA_BASE_URL = JIRA_CONFIG['JIRA_BASE_URL']
JIRA_API_TOKEN = JIRA_CONFIG['JIRA_API_TOKEN']
JIRA_EMAIL = JIRA_CONFIG['JIRA_USERNAME']
DEFAULT_PROJECT_KEY = JIRA_CONFIG['JIRA_PROJECT_KEY'] 