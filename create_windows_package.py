#!/usr/bin/env python3
"""
Create a Windows-compatible package that can be easily installed and run
"""
import os
import shutil
import zipfile

def create_windows_package():
    """Create a Windows package with all necessary files"""
    print("📦 Creating Windows package...")
    
    # Create package directory
    package_dir = "Axora-Windows-Package"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Copy main application file
    shutil.copy("utility_bill_organizer_pyqt6.py", f"{package_dir}/axora.py")
    
    # Copy Excel file
    shutil.copy("Bell-Rogers-Telus Login.xlsx", package_dir)
    
    # Copy icon
    shutil.copy("axora.ico", package_dir)
    
    # Create requirements.txt
    requirements = """PyQt6>=6.0.0
pandas>=1.3.0
openpyxl>=3.0.0
"""
    with open(f"{package_dir}/requirements.txt", "w") as f:
        f.write(requirements)
    
    # Create Windows batch installer
    installer_content = """@echo off
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
"""
    
    with open(f"{package_dir}/install.bat", "w") as f:
        f.write(installer_content)
    
    # Create Windows launcher
    launcher_content = """@echo off
echo Starting Axora...
python axora.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to start Axora
    echo Please run install.bat first to install dependencies
    pause
)
"""
    
    with open(f"{package_dir}/run-axora.bat", "w") as f:
        f.write(launcher_content)
    
    # Create PowerShell installer (alternative)
    ps_installer = """# Axora Installation Script for PowerShell
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
"""
    
    with open(f"{package_dir}/install.ps1", "w") as f:
        f.write(ps_installer)
    
    # Create comprehensive README
    readme_content = """# Axora - Utility Bill Organizer for Windows

## Quick Installation

### Method 1: Automatic Installation (Recommended)
1. Double-click `install.bat`
2. Follow the on-screen instructions
3. Run `run-axora.bat` to start the application

### Method 2: PowerShell Installation
1. Right-click `install.ps1` and select "Run with PowerShell"
2. Follow the on-screen instructions
3. Run `run-axora.bat` to start the application

### Method 3: Manual Installation
1. Install Python 3.8+ from https://python.org
2. Open Command Prompt in this folder
3. Run: `pip install -r requirements.txt`
4. Run: `python axora.py`

## System Requirements
- Windows 10 or later
- Python 3.8 or later
- Internet connection (for initial setup)

## Features
- Modern, intuitive interface
- Automatic bill organization by corporation, provider, account, and year
- Smart account number detection
- Support for Bell, Rogers, and Telus providers
- Excel integration for account mapping

## Troubleshooting

### "Python is not recognized"
- Install Python from https://python.org
- Make sure to check "Add Python to PATH" during installation
- Restart your computer after installation

### "Module not found" errors
- Run `install.bat` to install required packages
- Or manually run: `pip install -r requirements.txt`

### Application won't start
- Make sure all files are in the same folder
- Check that `Bell-Rogers-Telus Login.xlsx` is present
- Try running as Administrator

### Windows Defender warnings
- This is normal for unsigned applications
- Click "More info" then "Run anyway"
- Or add the folder to Windows Defender exclusions

## File Structure
```
Axora-Windows-Package/
├── axora.py                    # Main application
├── axora.ico                   # Application icon
├── Bell-Rogers-Telus Login.xlsx # Account mapping file
├── requirements.txt            # Python dependencies
├── install.bat                 # Windows installer
├── install.ps1                 # PowerShell installer
├── run-axora.bat              # Application launcher
└── README.txt                 # This file
```

## Support
- Website: https://axora-ak.vercel.app
- GitHub: https://github.com/AdityaKuchhal/Axora

## License
MIT License - See LICENSE file for details

---
Created by Aditya Kuchhal
"""
    
    with open(f"{package_dir}/README.txt", "w") as f:
        f.write(readme_content)
    
    # Create a simple setup script
    setup_script = """import sys
import subprocess
import os

def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def main():
    print("Axora - Utility Bill Organizer")
    print("Installing dependencies...")
    
    if install_requirements():
        print("\\n🎉 Setup complete! You can now run axora.py")
    else:
        print("\\n❌ Setup failed. Please install dependencies manually:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()
"""
    
    with open(f"{package_dir}/setup.py", "w") as f:
        f.write(setup_script)
    
    print(f"✅ Windows package created in '{package_dir}/'")
    return package_dir

def create_zip_package(package_dir):
    """Create a ZIP file for easy distribution"""
    print("📦 Creating ZIP package...")
    
    zip_filename = "Axora-Windows.zip"
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arc_path)
    
    file_size = os.path.getsize(zip_filename) / (1024 * 1024)  # Size in MB
    print(f"✅ ZIP package created: {zip_filename} ({file_size:.1f} MB)")
    return zip_filename

if __name__ == "__main__":
    print("🚀 Creating Windows-compatible package...")
    
    # Create package directory
    package_dir = create_windows_package()
    
    # Create ZIP file
    zip_file = create_zip_package(package_dir)
    
    print(f"\n🎉 Windows package ready!")
    print(f"📁 Package directory: {package_dir}/")
    print(f"📦 ZIP file: {zip_file}")
    print(f"\n💡 Users can download and extract the ZIP file to install Axora")
    print(f"   No compilation required - just Python and pip!")
