# Axora Installation Script for PowerShell
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Axora - Utility Bill Organizer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://python.org" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Install requirements
Write-Host "Installing required packages..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install required packages" -ForegroundColor Red
    Write-Host "Please check your internet connection and try again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Installation completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "To run Axora:" -ForegroundColor Cyan
Write-Host "1. Double-click 'run-axora.bat'" -ForegroundColor White
Write-Host "2. Or run: python axora.py" -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to exit"
