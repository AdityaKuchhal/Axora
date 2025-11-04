#!/usr/bin/env python3
"""
Build script for creating Windows executable
This script should be run on a Windows machine with Python installed.
"""
import subprocess
import sys
import os
import shutil

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("[OK] PyInstaller already installed")
    except ImportError:
        print("[*] Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_windows_exe():
    """Build Windows executable"""
    print("[*] Building Windows executable...")
    
    # Clean previous builds
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("Axora.spec"):
        os.remove("Axora.spec")
    
    # PyInstaller command for Windows
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window
        "--name", "Axora",
        "--icon", "assets/icons/axora.ico",
        "--hidden-import", "pandas",
        "--hidden-import", "openpyxl",
        "--hidden-import", "PyQt6",
        "--hidden-import", "PyQt6.QtCore",
        "--hidden-import", "PyQt6.QtWidgets",
        "--hidden-import", "PyQt6.QtGui",
        "axora.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("[OK] Windows executable created successfully!")
        print("[*] Output: dist/Axora.exe")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Build failed: {e}")
        return False

def main():
    """Main build process"""
    print("[*] Building Axora for Windows...")
    print("[!] Note: This script should be run on a Windows machine")
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Build executable
    if build_windows_exe():
        print("\n[SUCCESS] Build completed successfully!")
        print("[*] Your Windows executable is ready:")
        print("    - dist/Axora.exe")
        print("\n[INFO] Note: This is a single executable file that includes all dependencies.")
        print("    Users can run it directly without installing Python.")
    else:
        print("\n[ERROR] Build failed. Check the error messages above.")

if __name__ == "__main__":
    main()
