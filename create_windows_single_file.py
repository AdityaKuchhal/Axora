#!/usr/bin/env python3
"""
Create a single Windows file that contains everything needed
"""
import os
import shutil
import zipfile

def create_single_windows_file():
    """Create a single Windows file with embedded Python"""
    print("📦 Creating single Windows file...")
    
    # Create a self-contained Python script
    python_script = '''#!/usr/bin/env python3
"""
Axora - Utility Bill Organizer
Self-contained Windows application
"""
import sys
import os
import subprocess
import tempfile
import zipfile
import shutil
from pathlib import Path

def install_dependencies():
    """Install required Python packages"""
    try:
        import PyQt6
        import pandas
        import openpyxl
        print("✅ All dependencies already installed")
        return True
    except ImportError:
        print("📦 Installing required packages...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6", "pandas", "openpyxl"])
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False

def extract_application():
    """Extract the main application from embedded data"""
    # This will be replaced with the actual application code
    app_code = """
# Main application code will be embedded here
print("Axora - Utility Bill Organizer")
print("This is a placeholder for the main application")
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(app_code)
        return f.name

def main():
    """Main entry point"""
    print("🚀 Starting Axora...")
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Cannot proceed without dependencies")
        input("Press Enter to exit...")
        return
    
    # Extract and run application
    app_file = extract_application()
    try:
        # Import and run the main application
        exec(open(app_file).read())
    finally:
        # Clean up
        if os.path.exists(app_file):
            os.unlink(app_file)

if __name__ == "__main__":
    main()
'''
    
    # Create the single file
    with open("Axora-Windows.py", "w") as f:
        f.write(python_script)
    
    print("✅ Single Python file created: Axora-Windows.py")
    return "Axora-Windows.py"

def create_windows_batch_launcher():
    """Create a batch file launcher"""
    batch_content = """@echo off
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
"""
    
    with open("Run-Axora.bat", "w") as f:
        f.write(batch_content)
    
    print("✅ Batch launcher created: Run-Axora.bat")
    return "Run-Axora.bat"

def create_windows_package():
    """Create a complete Windows package"""
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
pause
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

## Features
- Modern, intuitive interface
- Automatic bill organization
- Support for Bell, Rogers, and Telus
- Excel integration

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
    print("🚀 Creating Windows single-file solution...")
    
    # Create single Python file
    single_file = create_single_windows_file()
    
    # Create batch launcher
    batch_launcher = create_windows_batch_launcher()
    
    # Create complete package
    package_dir = create_windows_package()
    
    # Create ZIP package
    zip_file = create_zip_package(package_dir)
    
    print(f"\n🎉 Windows solution ready!")
    print(f"📁 Single file: {single_file}")
    print(f"📁 Batch launcher: {batch_launcher}")
    print(f"📁 Complete package: {package_dir}/")
    print(f"📦 ZIP package: {zip_file}")
    print(f"\n💡 Users can download the ZIP file and run Install.bat")
