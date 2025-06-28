# Jira Ticket Manager - Quick Commands

## 🚀 One-Command Rebuild (Easiest)

```bash
./rebuild.sh
```

## 🔧 Manual Rebuild (Step by Step)

### 1. Set Environment

```bash
export PATH=$PATH:/Users/darkshadow/Library/Python/3.9/bin
```

### 2. Clean & Build

```bash
rm -rf dist/ build/ __pycache__/ && rm -f JiraTicketManager.spec
pyinstaller --onefile --name=JiraTicketManager --add-data=templates:templates --add-data=static:static --add-data=config.py:config.py --hidden-import=flask --hidden-import=flask_cors --hidden-import=pandas --hidden-import=requests --hidden-import=webview --hidden-import=threading --hidden-import=webbrowser --hidden-import=app --hidden-import=routes --hidden-import=controllers --hidden-import=jira_service --hidden-import=validation --hidden-import=helpers --hidden-import=config app.py
```

### 3. Create Distribution

```bash
mkdir -p JiraTicketManager_macOS && cp dist/JiraTicketManager JiraTicketManager_macOS/ && cp APP_README.md JiraTicketManager_macOS/ 2>/dev/null || echo "APP_README.md not found" && cp sample_tickets.xlsx JiraTicketManager_macOS/ 2>/dev/null || echo "sample_tickets.xlsx not found"
```

### 4. Create ZIP (Optional)

```bash
zip -r JiraTicketManager_macOS.zip JiraTicketManager_macOS/
```

## 🧪 Test Commands

### Test Executable

```bash
./dist/JiraTicketManager
```

### Check Dependencies

```bash
python3 -c "import flask, flask_cors, pandas, requests, webview, webbrowser; print('All dependencies OK')"
```

### Verify PyInstaller

```bash
pyinstaller --version
```

## 📁 File Locations

- **Executable**: `dist/JiraTicketManager`
- **Distribution**: `JiraTicketManager_macOS/`
- **ZIP Package**: `JiraTicketManager_macOS.zip`
- **Build Script**: `rebuild.sh`
- **Instructions**: `BUILD_INSTRUCTIONS.md`

## 🔄 When to Rebuild

- After changing any Python code
- After modifying templates or static files
- After updating dependencies
- Before distributing to users

## ⚡ Pro Tips

1. **Always use `./rebuild.sh`** for quick rebuilds
2. **Test the executable** after building
3. **Keep the distribution folder** for easy sharing
4. **Use the ZIP file** for email/cloud sharing

---

_Copy these commands for quick reference!_
