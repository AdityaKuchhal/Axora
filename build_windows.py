#!/usr/bin/env python3
"""
Build script for creating Windows executable with proper security and compatibility
"""
import subprocess
import sys
import os
import shutil

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def clean_build():
    """Clean previous build artifacts"""
    print("🧹 Cleaning previous build...")
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}/")

def build_executable():
    """Build Windows executable with proper security settings"""
    print("🔨 Building Windows executable...")
    
    # PyInstaller command with enhanced security and compatibility
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window
        "--name", "Axora",
        "--icon", "axora.ico",
        "--add-data", "Bell-Rogers-Telus Login.xlsx:.",  # Correct syntax for macOS building Windows
        "--hidden-import", "pandas",
        "--hidden-import", "openpyxl",
        "--hidden-import", "PyQt6",
        "--hidden-import", "PyQt6.QtCore",
        "--hidden-import", "PyQt6.QtWidgets",
        "--hidden-import", "PyQt6.QtGui",
        "--hidden-import", "PyQt6.QtOpenGL",
        "--hidden-import", "PyQt6.sip",
        "--collect-all", "PyQt6",  # Collect all PyQt6 modules
        "--noconfirm",  # Replace output directory without asking
        "--clean",  # Clean cache and remove temporary files
        "--log-level", "WARN",  # Reduce log verbosity
        # Security and compatibility options
        "--strip",  # Strip debug symbols to reduce size
        "--noupx",  # Disable UPX compression (can cause false positives)
        "--exclude-module", "tkinter",  # Exclude unused modules
        "--exclude-module", "matplotlib",
        "--exclude-module", "numpy.tests",
        "utility_bill_organizer_pyqt6.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Windows executable created successfully!")
        
        # Check if the executable was created
        exe_path = "dist/Axora.exe"
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)  # Size in MB
            print(f"📁 Output: {exe_path} ({file_size:.1f} MB)")
            return True
        else:
            print("❌ Executable not found after build")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

def create_version_info():
    """Create version info file for Windows executable"""
    version_info = """# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Aditya Kuchhal'),
        StringStruct(u'FileDescription', u'Axora - Utility Bill Organizer'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'Axora'),
        StringStruct(u'LegalCopyright', u'Copyright (C) 2024 Aditya Kuchhal'),
        StringStruct(u'OriginalFilename', u'Axora.exe'),
        StringStruct(u'ProductName', u'Axora'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    with open("version_info.txt", "w", encoding="utf-8") as f:
        f.write(version_info)
    print("📝 Created version info file")

def create_manifest():
    """Create application manifest for Windows compatibility"""
    manifest = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity version="1.0.0.0" processorArchitecture="*" name="Axora" type="win32"/>
  <description>Axora - Utility Bill Organizer</description>
  <dependency>
    <dependentAssembly>
      <assemblyIdentity type="win32" name="Microsoft.Windows.Common-Controls" version="6.0.0.0" processorArchitecture="*" publicKeyToken="6595b64144ccf1df" language="*"/>
    </dependentAssembly>
  </dependency>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v2">
    <security>
      <requestedPrivileges xmlns="urn:schemas-microsoft-com:asm.v3">
        <requestedExecutionLevel level="asInvoker" uiAccess="false"/>
      </requestedPrivileges>
    </security>
  </trustInfo>
  <compatibility xmlns="urn:schemas-microsoft-com:compatibility.v1">
    <application>
      <supportedOS Id="{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}"/>
      <supportedOS Id="{1f676c76-80e1-4239-95bb-83d0f6d0da78}"/>
      <supportedOS Id="{4a2f28e3-53b9-4441-ba9c-d69d4a4a6e38}"/>
      <supportedOS Id="{35138b9a-5d96-4fbd-8e2d-a2440225f93a}"/>
      <supportedOS Id="{e2011457-1546-43c5-a5fe-008deee3d3f0}"/>
    </application>
  </compatibility>
</assembly>"""
    
    with open("app.manifest", "w", encoding="utf-8") as f:
        f.write(manifest)
    print("📝 Created application manifest")

if __name__ == "__main__":
    print("🚀 Building Axora for Windows with enhanced security...")
    
    # Clean previous builds
    clean_build()
    
    # Install dependencies
    install_pyinstaller()
    
    # Create version info and manifest
    create_version_info()
    create_manifest()
    
    # Build executable
    if build_executable():
        print("\n🎉 Build completed successfully!")
        print("📦 Your Windows executable is ready in the 'dist' folder")
        print("💡 Note: Windows Defender may flag unsigned executables as harmful")
        print("   Users can add an exception or use 'Run as Administrator'")
    else:
        print("\n❌ Build failed. Check the error messages above.")