@echo off
echo ========================================
echo    Axora - Utility Bill Organizer
echo ========================================
echo.
echo This will install Axora on your Windows system.
echo.
echo Requirements:
echo - Python 3.8 or later
echo - Internet connection for package installation
echo.
pause

echo.
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found! Installing required packages...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Failed to install required packages
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo Installation completed successfully!
echo.
echo To run Axora:
echo 1. Double-click "run-axora.bat"
echo 2. Or run: python axora.py
echo.
pause
