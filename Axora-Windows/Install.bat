@echo off
title Axora Installer
echo.
echo ========================================
echo    Axora - Utility Bill Organizer
echo ========================================
echo.
echo This will install Axora on your system.
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Installing required packages...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

echo.
echo ✅ Installation completed!
echo.
echo To run Axora, double-click "Run-Axora.bat"
echo.
pause
