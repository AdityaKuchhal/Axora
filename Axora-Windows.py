#!/usr/bin/env python3
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
