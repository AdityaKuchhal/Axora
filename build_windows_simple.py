#!/usr/bin/env python3
"""
Simple Windows build script - creates a Windows-compatible executable
"""
import subprocess
import sys
import os
import shutil

def clean_build():
    """Clean previous build artifacts"""
    print("🧹 Cleaning previous build...")
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}/")

def build_windows_executable():
    """Build Windows executable with minimal dependencies"""
    print("🔨 Building Windows executable...")
    
    # Simplified PyInstaller command for better Windows compatibility
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--console",  # Keep console for debugging
        "--name", "Axora",
        "--icon", "axora.ico",
        "--add-data", "Bell-Rogers-Telus Login.xlsx:.",  # Add Excel file
        "--hidden-import", "pandas",
        "--hidden-import", "openpyxl",
        "--hidden-import", "PyQt6",
        "--hidden-import", "PyQt6.QtCore",
        "--hidden-import", "PyQt6.QtWidgets",
        "--hidden-import", "PyQt6.QtGui",
        "--noconfirm",
        "--clean",
        "--noupx",  # Disable UPX to avoid false positives
        "utility_bill_organizer_pyqt6.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Windows executable created successfully!")
        
        # Check if the executable was created
        exe_path = "dist/Axora"
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)  # Size in MB
            print(f"📁 Output: {exe_path} ({file_size:.1f} MB)")
            
            # Rename to .exe for Windows compatibility
            exe_path_renamed = "dist/Axora.exe"
            if os.path.exists(exe_path_renamed):
                os.remove(exe_path_renamed)
            os.rename(exe_path, exe_path_renamed)
            print(f"📁 Renamed to: {exe_path_renamed}")
            return True
        else:
            print("❌ Executable not found after build")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

def create_windows_launcher():
    """Create a Windows batch file launcher"""
    print("📝 Creating Windows launcher...")
    
    launcher_content = """@echo off
echo Starting Axora...
echo.
echo If Windows Defender flags this as harmful:
echo 1. Click "More info"
echo 2. Click "Run anyway"
echo.
pause
Axora.exe
pause
"""
    
    with open("dist/Start-Axora.bat", "w") as f:
        f.write(launcher_content)
    
    print("✅ Windows launcher created: Start-Axora.bat")

def create_readme():
    """Create installation instructions"""
    print("📝 Creating installation instructions...")
    
    readme_content = """# Axora - Windows Installation Guide

## Quick Start
1. Download `Axora.exe` and `Start-Axora.bat`
2. Place both files in the same folder
3. Double-click `Start-Axora.bat` to run Axora

## If Windows Defender Flags as Harmful
This is a false positive because the executable is not code-signed. To run:

### Method 1: Use the Batch File
- Double-click `Start-Axora.bat` instead of `Axora.exe` directly

### Method 2: Add Exception
1. When Windows Defender blocks the file, click "More info"
2. Click "Run anyway"
3. The app will start normally

### Method 3: Add to Exclusions
1. Open Windows Security
2. Go to Virus & threat protection
3. Click "Manage settings" under Virus & threat protection settings
4. Click "Add or remove exclusions"
5. Click "Add an exclusion" > "File"
6. Select `Axora.exe`

## System Requirements
- Windows 10 or later
- No additional software required
- Internet connection for initial setup

## Troubleshooting
- If the app doesn't start, try running as Administrator
- Make sure `Bell-Rogers-Telus Login.xlsx` is in the same folder
- Check that Windows Defender isn't blocking the file

## Support
Visit: https://axora-ak.vercel.app
"""
    
    with open("dist/README-Windows.txt", "w") as f:
        f.write(readme_content)
    
    print("✅ Installation guide created: README-Windows.txt")

if __name__ == "__main__":
    print("🚀 Building Axora for Windows (Simple Version)...")
    
    # Clean previous builds
    clean_build()
    
    # Build executable
    if build_windows_executable():
        print("\n🎉 Build completed successfully!")
        
        # Create additional files
        create_windows_launcher()
        create_readme()
        
        print("\n📦 Windows files ready:")
        print("   - Axora.exe (main application)")
        print("   - Start-Axora.bat (launcher)")
        print("   - README-Windows.txt (instructions)")
        print("\n💡 Note: Windows Defender may flag unsigned executables")
        print("   Use the batch file launcher or add an exception")
    else:
        print("\n❌ Build failed. Check the error messages above.")
