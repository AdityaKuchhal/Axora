#!/usr/bin/env python3
"""
Master build script for Axora
Creates executables for both platforms and prepares website files
"""
import subprocess
import sys
import os
import shutil
import zipfile
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔨 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing build dependencies...")
    
    dependencies = [
        "pyinstaller",
        "pandas",
        "openpyxl",
        "PyQt6"
    ]
    
    for dep in dependencies:
        if not run_command(f"{sys.executable} -m pip install {dep}", f"Installing {dep}"):
            return False
    
    return True

def build_windows():
    """Build Windows executable"""
    print("\n🪟 Building Windows executable...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "Axora",
        "--icon", "axora.ico",
        "--add-data", "Bell-Rogers-Telus Login.xlsx;.",
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
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Windows build failed: {e}")
        return False

def build_macos():
    """Build macOS app bundle"""
    print("\n🍎 Building macOS app bundle...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "Axora",
        "--icon", "axora.icns",
        "--add-data", "Bell-Rogers-Telus Login.xlsx:.",
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
        
        # Create .app bundle
        create_macos_app_bundle()
        print("✅ macOS app bundle created successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ macOS build failed: {e}")
        return False

def create_macos_app_bundle():
    """Create proper macOS .app bundle"""
    app_name = "Axora.app"
    app_path = f"dist/{app_name}"
    
    # Create app bundle structure
    os.makedirs(f"{app_path}/Contents/MacOS", exist_ok=True)
    os.makedirs(f"{app_path}/Contents/Resources", exist_ok=True)
    
    # Move executable
    if os.path.exists("dist/Axora"):
        os.rename("dist/Axora", f"{app_path}/Contents/MacOS/Axora")
    
    # Create Info.plist
    info_plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>Axora</string>
    <key>CFBundleIdentifier</key>
    <string>com.adityakuchhal.axora</string>
    <key>CFBundleName</key>
    <string>Axora</string>
    <key>CFBundleVersion</key>
    <string>2.1</string>
    <key>CFBundleShortVersionString</key>
    <string>2.1</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>CFBundleIconFile</key>
    <string>axora</string>
    <key>LSApplicationCategoryType</key>
    <string>public.app-category.productivity</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSRequiresAquaSystemAppearance</key>
    <false/>
</dict>
</plist>"""
    
    with open(f"{app_path}/Contents/Info.plist", "w") as f:
        f.write(info_plist)
    
    # Remove quarantine attributes to prevent "damaged" error
    print("🔓 Removing quarantine attributes...")
    try:
        subprocess.run(["xattr", "-d", "com.apple.quarantine", app_path], check=False)
        subprocess.run(["xattr", "-d", "com.apple.metadata:kMDItemWhereFroms", app_path], check=False)
        print("✅ Quarantine attributes removed")
    except Exception as e:
        print(f"⚠️  Could not remove quarantine attributes: {e}")
    
    # Make executable
    os.chmod(f"{app_path}/Contents/MacOS/Axora", 0o755)

def create_downloads_folder():
    """Create downloads folder and prepare files"""
    print("\n📁 Preparing download files...")
    
    # Create downloads directory
    os.makedirs("downloads", exist_ok=True)
    
    # Copy website files
    if os.path.exists("index.html"):
        shutil.copy("index.html", "downloads/")
    
    # Prepare Windows executable
    if os.path.exists("dist/Axora.exe"):
        shutil.copy("dist/Axora.exe", "downloads/Axora-Windows.exe")
        print("✅ Windows executable ready for download")
    
    # Prepare macOS app bundle
    if os.path.exists("dist/Axora.app"):
        # Create zip file for macOS
        with zipfile.ZipFile("downloads/Axora-macOS.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk("dist/Axora.app"):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_path = os.path.relpath(file_path, "dist")
                    zipf.write(file_path, arc_path)
        print("✅ macOS app bundle ready for download")
    
    # Create README for downloads
    readme_content = """# Axora - Utility Bill Organizer

## Installation

### Windows
1. Download `Axora-Windows.exe`
2. Double-click to run
3. No additional installation required

### macOS
1. Download `Axora-macOS.zip`
2. Extract the zip file
3. Move `Axora.app` to your Applications folder
4. Double-click to run

## Usage
1. Select your Excel file with corporation/provider mappings
2. Choose source folder containing utility bills
3. Select destination Utilities folder
4. Click Execute to organize files

## Features
- Automatic file organization
- Smart year-based folder structure
- Progress tracking
- History logging
- Dark/Light themes
- Cross-platform support

## Support
For issues or questions, please contact AK Realm.

© 2024 AK Realm. All rights reserved.
"""
    
    with open("downloads/README.txt", "w") as f:
        f.write(readme_content)
    
    print("✅ Download files prepared successfully")

def cleanup():
    """Clean up build artifacts"""
    print("\n🧹 Cleaning up build artifacts...")
    
    # Remove build directories
    for dir_name in ["build", "__pycache__"]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ Removed {dir_name}")
    
    # Remove spec files
    for spec_file in ["Axora.spec"]:
        if os.path.exists(spec_file):
            os.remove(spec_file)
            print(f"✅ Removed {spec_file}")

def main():
    """Main build process"""
    print("🚀 Starting Axora build process...")
    print("=" * 50)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return False
    
    # Build for current platform
    current_platform = sys.platform
    
    if current_platform == "win32":
        if not build_windows():
            print("❌ Windows build failed")
            return False
    elif current_platform == "darwin":
        if not build_macos():
            print("❌ macOS build failed")
            return False
    else:
        print(f"⚠️  Unsupported platform: {current_platform}")
        print("Building for Windows anyway...")
        if not build_windows():
            print("❌ Windows build failed")
            return False
    
    # Create downloads folder
    create_downloads_folder()
    
    # Cleanup
    cleanup()
    
    print("\n" + "=" * 50)
    print("🎉 Build process completed successfully!")
    print("\n📦 Output files:")
    print("  - downloads/Axora-Windows.exe (Windows)")
    print("  - downloads/Axora-macOS.zip (macOS)")
    print("  - downloads/index.html (Website)")
    print("  - downloads/README.txt (Instructions)")
    
    print("\n🌐 To deploy the website:")
    print("  1. Upload the 'downloads' folder to your web server")
    print("  2. Make sure the executable files are accessible")
    print("  3. Update download links in index.html if needed")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

