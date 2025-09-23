@echo off
title Axora - Utility Bill Organizer
echo.
echo ========================================
echo    Axora - Utility Bill Organizer
echo ========================================
echo.
echo Starting Axora...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Run the application
python Axora-Windows.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Application failed to start
    echo Please check the error messages above
    echo.
    pause
)

echo.
echo Axora has closed.
pause
