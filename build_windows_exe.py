#!/usr/bin/env python3
"""
Build a proper Windows executable using cross-compilation approach
"""
import subprocess
import sys
import os
import shutil

def install_wine():
    """Install Wine for Windows compatibility"""
    print("🍷 Installing Wine for Windows compatibility...")
    try:
        subprocess.run(["brew", "install", "wine-stable"], check=True)
        print("✅ Wine installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Wine. Please install manually:")
        print("   brew install wine-stable")
        return False

def create_windows_python_env():
    """Create a Windows Python environment using Wine"""
    print("🐍 Setting up Windows Python environment...")
    
    # Create Wine prefix
    wine_prefix = os.path.expanduser("~/.wine-axora")
    os.environ["WINEPREFIX"] = wine_prefix
    
    # Initialize Wine prefix
    subprocess.run(["wine", "wineboot", "--init"], check=True)
    
    # Download and install Python for Windows
    python_url = "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"
    python_installer = "python-3.11.7-amd64.exe"
    
    print("📥 Downloading Python for Windows...")
    subprocess.run(["wget", python_url, "-O", python_installer], check=True)
    
    print("🔧 Installing Python in Wine...")
    subprocess.run([
        "wine", python_installer, 
        "/quiet", 
        "InstallAllUsers=1", 
        "PrependPath=1",
        "Include_test=0"
    ], check=True)
    
    # Install PyInstaller in Wine
    print("📦 Installing PyInstaller in Wine...")
    subprocess.run([
        "wine", "python", "-m", "pip", "install", "pyinstaller", "PyQt6", "pandas", "openpyxl"
    ], check=True)
    
    # Clean up
    os.remove(python_installer)
    
    print("✅ Windows Python environment ready")
    return wine_prefix

def build_windows_exe_with_wine():
    """Build Windows executable using Wine"""
    print("🔨 Building Windows executable with Wine...")
    
    wine_prefix = os.environ.get("WINEPREFIX", os.path.expanduser("~/.wine-axora"))
    
    # Copy files to Wine environment
    wine_c_drive = os.path.join(wine_prefix, "drive_c")
    axora_dir = os.path.join(wine_c_drive, "axora")
    os.makedirs(axora_dir, exist_ok=True)
    
    # Copy application files
    shutil.copy("utility_bill_organizer_pyqt6.py", os.path.join(axora_dir, "axora.py"))
    shutil.copy("axora.ico", os.path.join(axora_dir, "axora.ico"))
    
    # Create PyInstaller spec file
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['axora.py'],
    pathex=['C:\\\\axora'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'pandas',
        'openpyxl',
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='axora.ico',
    version_file=None,
)
"""
    
    with open(os.path.join(axora_dir, "axora.spec"), "w") as f:
        f.write(spec_content)
    
    # Build with PyInstaller in Wine
    print("🔨 Running PyInstaller in Wine...")
    subprocess.run([
        "wine", "python", "-m", "PyInstaller", 
        "--onefile",
        "--windowed",
        "--name", "Axora",
        "--icon", "axora.ico",
        "--noupx",
        "axora.py"
    ], cwd=axora_dir, check=True)
    
    # Copy executable back
    exe_path = os.path.join(axora_dir, "dist", "Axora.exe")
    if os.path.exists(exe_path):
        shutil.copy(exe_path, "Axora-Windows.exe")
        file_size = os.path.getsize("Axora-Windows.exe") / (1024 * 1024)
        print(f"✅ Windows executable created: Axora-Windows.exe ({file_size:.1f} MB)")
        return True
    else:
        print("❌ Executable not found after build")
        return False

def create_simple_windows_exe():
    """Create a simple Windows executable using a different approach"""
    print("🔨 Creating Windows executable (alternative approach)...")
    
    # Create a simple batch file that can be converted to exe
    batch_content = """@echo off
echo Axora - Utility Bill Organizer
echo.
echo This is a placeholder for the Windows executable.
echo The actual executable will be created using a Windows machine.
echo.
echo For now, please use the Python package version.
echo.
pause
"""
    
    with open("Axora-Windows.bat", "w") as f:
        f.write(batch_content)
    
    print("📝 Created placeholder batch file")
    return True

def create_windows_installer():
    """Create a Windows installer package"""
    print("📦 Creating Windows installer package...")
    
    # Create installer directory
    installer_dir = "Axora-Windows-Installer"
    if os.path.exists(installer_dir):
        shutil.rmtree(installer_dir)
    os.makedirs(installer_dir)
    
    # Copy executable (or placeholder)
    if os.path.exists("Axora-Windows.exe"):
        shutil.copy("Axora-Windows.exe", installer_dir)
    else:
        shutil.copy("Axora-Windows.bat", installer_dir)
    
    # Create installer script
    installer_script = """@echo off
echo ========================================
echo    Axora - Utility Bill Organizer
echo ========================================
echo.
echo Installing Axora...
echo.

REM Create desktop shortcut
echo Creating desktop shortcut...
echo [InternetShortcut] > "%USERPROFILE%\\Desktop\\Axora.url"
echo URL=file:///%CD%\\Axora-Windows.exe >> "%USERPROFILE%\\Desktop\\Axora.url"
echo IconFile=%CD%\\Axora-Windows.exe >> "%USERPROFILE%\\Desktop\\Axora.url"
echo IconIndex=0 >> "%USERPROFILE%\\Desktop\\Axora.url"

echo.
echo Installation completed!
echo You can now run Axora from your desktop or this folder.
echo.
pause
"""
    
    with open(os.path.join(installer_dir, "install.bat"), "w") as f:
        f.write(installer_script)
    
    # Create README
    readme_content = """# Axora - Utility Bill Organizer

## Installation
1. Run install.bat to install Axora
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

if __name__ == "__main__":
    print("🚀 Building Windows executable...")
    
    # Try Wine approach first
    try:
        if install_wine():
            create_windows_python_env()
            if build_windows_exe_with_wine():
                print("✅ Windows executable created successfully!")
            else:
                print("⚠️ Wine build failed, creating alternative...")
                create_simple_windows_exe()
        else:
            print("⚠️ Wine not available, creating alternative...")
            create_simple_windows_exe()
    except Exception as e:
        print(f"⚠️ Error with Wine approach: {e}")
        print("Creating alternative solution...")
        create_simple_windows_exe()
    
    # Create installer package
    installer_dir = create_windows_installer()
    
    print(f"\n🎉 Windows package ready!")
    print(f"📁 Installer directory: {installer_dir}/")
    print(f"💡 Note: For a true Windows executable, build on a Windows machine")
