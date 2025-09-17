#!/usr/bin/env python3
"""
Build script for creating Windows executable
"""
import subprocess
import sys
import os

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_executable():
    """Build Windows executable"""
    print("🔨 Building Windows executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window
        "--name", "Axora",
        "--icon", "axora.ico",  # Add icon
        "--add-data", "Bell-Rogers-Telus Login.xlsx;.",  # Add Excel file
        "--hidden-import", "pandas",
        "--hidden-import", "openpyxl",
        "--hidden-import", "PyQt6",
        "--hidden-import", "PyQt6.QtCore",
        "--hidden-import", "PyQt6.QtWidgets",
        "--hidden-import", "PyQt6.QtGui",
        "utility_bill_organizer_pyqt6.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Windows executable created successfully!")
        print("📁 Output: dist/Axora.exe")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    
    return True

def create_icon():
    """Create a simple icon file"""
    print("🎨 Creating icon...")
    # For now, we'll skip the icon creation
    # In a real scenario, you'd create an .ico file
    pass

if __name__ == "__main__":
    print("🚀 Building Axora for Windows...")
    
    # Install dependencies
    install_pyinstaller()
    
    # Create icon (optional)
    create_icon()
    
    # Build executable
    if build_executable():
        print("\n🎉 Build completed successfully!")
        print("📦 Your Windows executable is ready in the 'dist' folder")
    else:
        print("\n❌ Build failed. Check the error messages above.")

