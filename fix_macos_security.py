#!/usr/bin/env python3
"""
Fix macOS security issues for Axora app
"""
import subprocess
import os
import sys

def fix_macos_security():
    """Fix macOS security issues"""
    print("🔧 Fixing macOS security issues for Axora...")
    
    app_path = "dist/Axora.app"
    
    if not os.path.exists(app_path):
        print("❌ Axora.app not found in dist/ folder")
        print("Please run the build first: python3 build_all.py")
        return False
    
    try:
        # Remove quarantine attributes
        print("🔓 Removing quarantine attributes...")
        subprocess.run(["xattr", "-d", "com.apple.quarantine", app_path], check=False)
        subprocess.run(["xattr", "-d", "com.apple.metadata:kMDItemWhereFroms", app_path], check=False)
        
        # Remove all extended attributes
        print("🧹 Removing all extended attributes...")
        subprocess.run(["xattr", "-cr", app_path], check=False)
        
        # Set proper permissions
        print("🔐 Setting proper permissions...")
        subprocess.run(["chmod", "-R", "755", app_path], check=True)
        
        # Make executable
        executable_path = f"{app_path}/Contents/MacOS/Axora"
        if os.path.exists(executable_path):
            subprocess.run(["chmod", "+x", executable_path], check=True)
        
        print("✅ Security fixes applied successfully!")
        print("\n📋 Next steps:")
        print("1. Right-click on Axora.app")
        print("2. Select 'Open' from the context menu")
        print("3. Click 'Open' when prompted")
        print("\nIf it still doesn't work, try:")
        print("1. Go to System Preferences → Security & Privacy")
        print("2. Click 'General' tab")
        print("3. Look for Axora and click 'Open Anyway'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing security issues: {e}")
        return False

if __name__ == "__main__":
    fix_macos_security()


