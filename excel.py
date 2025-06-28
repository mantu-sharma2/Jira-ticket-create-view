import pandas as pd
import os

# Define the data
data = [
    {
        "summary": "Login fails",
        "description": "User cannot login",
        "issue_type": "Bug",
        "priority": "High",
        "project_key": "PROJ1",
        "assignee": "alice",
        "labels": "auth,urgent"
    },
    {
        "summary": "UI glitch",
        "description": "Button misaligned",
        "issue_type": "Bug",
        "priority": "Medium",
        "project_key": "PROJ1",
        "assignee": "bob",
        "labels": "ui,frontend"
    },
    {
        "summary": "Add feature X",
        "description": "Request for feature X",
        "issue_type": "Task",
        "priority": "Low",
        "project_key": "PROJ2",
        "assignee": "carol",
        "labels": "enhancement"
    },
    {
        "summary": "API timeout",
        "description": "API call times out",
        "issue_type": "Bug",
        "priority": "High",
        "project_key": "PROJ2",
        "assignee": "dave",
        "labels": "backend,api"
    },
    {
        "summary": "Update docs",
        "description": "Documentation outdated",
        "issue_type": "Task",
        "priority": "Low",
        "project_key": "PROJ3",
        "assignee": "eve",
        "labels": "docs"
    },
    {
        "summary": "Crash on save",
        "description": "App crashes on save",
        "issue_type": "Bug",
        "priority": "Critical",
        "project_key": "PROJ1",
        "assignee": "frank",
        "labels": "crash,urgent"
    },
    {
        "summary": "Improve speed",
        "description": "App is slow to load",
        "issue_type": "Task",
        "priority": "Medium",
        "project_key": "PROJ2",
        "assignee": "grace",
        "labels": "performance"
    },
    {
        "summary": "Email not sent",
        "description": "Email notifications fail",
        "issue_type": "Bug",
        "priority": "High",
        "project_key": "PROJ3",
        "assignee": "heidi",
        "labels": "email,backend"
    },
    {
        "summary": "Add dark mode",
        "description": "Request for dark mode",
        "issue_type": "Task",
        "priority": "Low",
        "project_key": "PROJ1",
        "assignee": "ivan",
        "labels": "ui,feature"
    },
    {
        "summary": "Fix typo",
        "description": "Typo in welcome message",
        "issue_type": "Bug",
        "priority": "Low",
        "project_key": "PROJ2",
        "assignee": "judy",
        "labels": "typo,frontend"
    }
]

# Create DataFrame and save to Excel
df = pd.DataFrame(data)
filename = "sample_tickets.xlsx"
df.to_excel(filename, index=False)
print(f"Created {filename}")
