@echo off
title Axora - Utility Bill Organizer
echo Starting Axora...
python axora.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to start Axora
    echo Please run Install.bat first to install dependencies
    pause
)
