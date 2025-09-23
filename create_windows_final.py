#!/usr/bin/env python3
"""
Create final Windows package without Excel file
"""
import os
import shutil
import zipfile

def create_windows_package():
    """Create Windows package without Excel file"""
    print("📦 Creating Windows package...")
    
    package_dir = "Axora-Windows"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Copy the main application file
    shutil.copy("utility_bill_organizer_pyqt6.py", os.path.join(package_dir, "axora.py"))
    
    # Copy icon
    shutil.copy("axora.ico", package_dir)
    
    # Create requirements file
    requirements = """PyQt6>=6.0.0
pandas>=1.3.0
openpyxl>=3.0.0
"""
    with open(os.path.join(package_dir, "requirements.txt"), "w") as f:
        f.write(requirements)
    
    # Create installer
    installer_content = """@echo off
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
"""
    
    with open(os.path.join(package_dir, "Install.bat"), "w") as f:
        f.write(installer_content)
    
    # Create launcher
    launcher_content = """@echo off
title Axora - Utility Bill Organizer
echo Starting Axora...
python axora.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to start Axora
    echo Please run Install.bat first to install dependencies
    pause
)
"""
    
    with open(os.path.join(package_dir, "Run-Axora.bat"), "w") as f:
        f.write(launcher_content)
    
    # Create README
    readme_content = """# Axora - Utility Bill Organizer

## Quick Start
1. Double-click "Install.bat" to install dependencies
2. Double-click "Run-Axora.bat" to start the application

## Manual Installation
1. Install Python 3.8+ from https://python.org
2. Open Command Prompt in this folder
3. Run: pip install -r requirements.txt
4. Run: python axora.py

## Requirements
- Windows 10 or later
- Python 3.8 or later
- Internet connection (for initial setup)

## Usage
1. Download your Excel file with account mappings
2. Select your source folder with bills
3. Select destination folder for organized bills
4. Click Execute to organize your bills

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
- Run Install.bat to install required packages
- Or manually run: pip install -r requirements.txt

### Application won't start
- Make sure all files are in the same folder
- Check that you have an Excel file with account mappings
- Try running as Administrator

## Support
Visit: https://axora-ak.vercel.app
"""
    
    with open(os.path.join(package_dir, "README.txt"), "w") as f:
        f.write(readme_content)
    
    print(f"✅ Windows package created in '{package_dir}/'")
    return package_dir

def create_zip_package(package_dir):
    """Create ZIP package for distribution"""
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
    
    file_size = os.path.getsize(zip_filename) / (1024 * 1024)
    print(f"✅ ZIP package created: {zip_filename} ({file_size:.1f} MB)")
    return zip_filename

if __name__ == "__main__":
    print("🚀 Creating final Windows package...")
    
    # Create package
    package_dir = create_windows_package()
    
    # Create ZIP package
    zip_file = create_zip_package(package_dir)
    
    print(f"\n🎉 Windows package ready!")
    print(f"📁 Package directory: {package_dir}/")
    print(f"📦 ZIP package: {zip_file}")
    print(f"\n💡 Note: Excel file not included - users provide their own")
    print(f"   This is a single-file solution that works on any Windows machine")
