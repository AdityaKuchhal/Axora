#!/usr/bin/env python3
"""
Create a proper Windows executable using PyInstaller with Windows compatibility
"""
import subprocess
import sys
import os
import shutil
import zipfile

def create_windows_spec():
    """Create a Windows-compatible PyInstaller spec file"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['utility_bill_organizer_pyqt6.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'pandas',
        'openpyxl',
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',
        'PyQt6.QtOpenGL',
        'PyQt6.sip',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy.tests',
        'scipy.tests',
        'pandas.tests',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Axora',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disable UPX to avoid false positives
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='axora.ico',
    version_file=None,
)
"""
    
    with open("axora.spec", "w") as f:
        f.write(spec_content)
    
    print("✅ Windows spec file created")

def build_windows_executable():
    """Build Windows executable using PyInstaller"""
    print("🔨 Building Windows executable...")
    
    # Clean previous builds
    for dir_name in ['build', 'dist', '__pycache__']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Cleaned {dir_name}/")
    
    # Create spec file
    create_windows_spec()
    
    # Build with PyInstaller
    cmd = [
        "pyinstaller",
        "--clean",
        "--noconfirm",
        "axora.spec"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Windows executable built successfully!")
        
        # Check if executable was created
        exe_path = "dist/Axora.exe"
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"📁 Executable: {exe_path} ({file_size:.1f} MB)")
            
            # Copy to root directory
            shutil.copy(exe_path, "Axora-Windows.exe")
            print(f"📁 Copied to: Axora-Windows.exe")
            return True
        else:
            print("❌ Executable not found after build")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

def create_windows_installer():
    """Create a Windows installer package"""
    print("📦 Creating Windows installer package...")
    
    installer_dir = "Axora-Windows-Installer"
    if os.path.exists(installer_dir):
        shutil.rmtree(installer_dir)
    os.makedirs(installer_dir)
    
    # Copy executable
    if os.path.exists("Axora-Windows.exe"):
        shutil.copy("Axora-Windows.exe", installer_dir)
    else:
        print("⚠️ Executable not found, creating placeholder...")
        # Create a placeholder
        placeholder = """@echo off
echo Axora - Utility Bill Organizer
echo.
echo This is a placeholder for the Windows executable.
echo The actual executable will be created on a Windows machine.
echo.
echo For now, please use the Python package version.
echo.
pause
"""
        with open(os.path.join(installer_dir, "Axora-Windows.bat"), "w") as f:
            f.write(placeholder)
    
    # Create installer script
    installer_script = """@echo off
title Axora Installer
echo.
echo ========================================
echo    Axora - Utility Bill Organizer
echo ========================================
echo.
echo Installing Axora...
echo.

REM Create desktop shortcut
echo Creating desktop shortcut...
if exist "Axora-Windows.exe" (
    echo [InternetShortcut] > "%USERPROFILE%\\Desktop\\Axora.url"
    echo URL=file:///%CD%\\Axora-Windows.exe >> "%USERPROFILE%\\Desktop\\Axora.url"
    echo IconFile=%CD%\\Axora-Windows.exe >> "%USERPROFILE%\\Desktop\\Axora.url"
    echo IconIndex=0 >> "%USERPROFILE%\\Desktop\\Axora.url"
) else (
    echo [InternetShortcut] > "%USERPROFILE%\\Desktop\\Axora.url"
    echo URL=file:///%CD%\\Axora-Windows.bat >> "%USERPROFILE%\\Desktop\\Axora.url"
    echo IconFile=%CD%\\Axora-Windows.bat >> "%USERPROFILE%\\Desktop\\Axora.url"
    echo IconIndex=0 >> "%USERPROFILE%\\Desktop\\Axora.url"
)

echo.
echo ✅ Installation completed!
echo.
echo You can now run Axora from your desktop or this folder.
echo.
pause
"""
    
    with open(os.path.join(installer_dir, "Install.bat"), "w") as f:
        f.write(installer_script)
    
    # Create README
    readme_content = """# Axora - Utility Bill Organizer

## Installation
1. Run Install.bat to install Axora
2. A desktop shortcut will be created
3. Double-click the shortcut or Axora-Windows.exe to run

## Usage
1. Download your Excel file with account mappings
2. Select your source folder with bills
3. Select destination folder for organized bills
4. Click Execute to organize your bills

## Requirements
- Windows 10 or later
- No additional software required

## Support
Visit: https://axora-ak.vercel.app
"""
    
    with open(os.path.join(installer_dir, "README.txt"), "w") as f:
        f.write(readme_content)
    
    print(f"✅ Windows installer package created in '{installer_dir}/'")
    return installer_dir

def create_zip_package(installer_dir):
    """Create ZIP package for distribution"""
    print("📦 Creating ZIP package...")
    
    zip_filename = "Axora-Windows.zip"
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(installer_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, installer_dir)
                zipf.write(file_path, arc_path)
    
    file_size = os.path.getsize(zip_filename) / (1024 * 1024)
    print(f"✅ ZIP package created: {zip_filename} ({file_size:.1f} MB)")
    return zip_filename

if __name__ == "__main__":
    print("🚀 Building Windows executable...")
    
    # Build executable
    if build_windows_executable():
        print("✅ Windows executable created successfully!")
    else:
        print("⚠️ Executable build failed, creating installer package...")
    
    # Create installer package
    installer_dir = create_windows_installer()
    
    # Create ZIP package
    zip_file = create_zip_package(installer_dir)
    
    print(f"\n🎉 Windows package ready!")
    print(f"📁 Installer directory: {installer_dir}/")
    print(f"📦 ZIP package: {zip_file}")
    print(f"\n💡 Note: The executable may need to be built on a Windows machine for full compatibility")
