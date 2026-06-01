@echo off
echo Uninstalling Smash...

:: Remove Registry Key
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "SmashApp" /f

:: Kill the process if running
taskkill /f /im Smash.exe

echo Smash has been removed from Windows Startup and killed.
pause
