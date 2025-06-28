@echo off
REM Jira Ticket Manager - Windows Installer

echo Installing Jira Ticket Manager...

REM Create application directory
set APP_DIR=%USERPROFILE%\JiraTicketManager
if not exist "%APP_DIR%" mkdir "%APP_DIR%"

REM Copy executable
copy "JiraTicketManager.exe" "%APP_DIR%\"

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Jira Ticket Manager.lnk'); $Shortcut.TargetPath = '%APP_DIR%\JiraTicketManager.exe'; $Shortcut.Save()"

echo Installation completed!
echo Application installed to: %APP_DIR%
echo.
echo To run the application:
echo   - Double-click the desktop shortcut, or
echo   - Run: %APP_DIR%\JiraTicketManager.exe
pause
