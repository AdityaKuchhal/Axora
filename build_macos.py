#!/usr/bin/env python3
"""
Build script for creating macOS app bundle
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

def build_app_bundle():
    """Build macOS app bundle"""
    print("🔨 Building macOS app bundle...")
    
    # PyInstaller command for macOS
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window
        "--name", "Axora",
        "--icon", "axora.icns",  # macOS icon format
        "--add-data", "Bell-Rogers-Telus Login.xlsx:.",  # Include Excel file
        "--hidden-import", "pandas",
        "--hidden-import", "openpyxl",
        "--hidden-import", "PyQt6",
        "utility_bill_organizer_pyqt6.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ macOS app bundle created successfully!")
        print("📁 Output: dist/Axora")
        
        # Create .app bundle
        create_app_bundle()
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    
    return True

def create_app_bundle():
    """Create proper macOS .app bundle"""
    print("📦 Creating macOS .app bundle...")
    
    app_name = "Axora.app"
    app_path = f"dist/{app_name}"
    
    # Create app bundle structure
    os.makedirs(f"{app_path}/Contents/MacOS", exist_ok=True)
    os.makedirs(f"{app_path}/Contents/Resources", exist_ok=True)
    
    # Move executable
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
    
    print(f"✅ macOS app bundle created: {app_path}")

def create_icon():
    """Create a simple icon file"""
    print("🎨 Creating icon...")
    # For now, we'll skip the icon creation
    # In a real scenario, you'd create an .icns file
    pass

if __name__ == "__main__":
    print("🚀 Building Axora for macOS...")
    
    # Install dependencies
    install_pyinstaller()
    
    # Create icon (optional)
    create_icon()
    
    # Build app bundle
    if build_app_bundle():
        print("\n🎉 Build completed successfully!")
        print("📦 Your macOS app bundle is ready in the 'dist' folder")
    else:
        print("\n❌ Build failed. Check the error messages above.")

