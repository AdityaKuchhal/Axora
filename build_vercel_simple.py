#!/usr/bin/env python3
"""
Simple build for Vercel deployment (without macOS app for now)
"""
import os
import shutil
import subprocess
import sys

def build_for_vercel_simple():
    """Build Axora for Vercel deployment (simple version)"""
    print("🚀 Building Axora for Vercel deployment (simple version)...")
    
    # Create public directory (Vercel's default)
    public_dir = "public"
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.makedirs(public_dir, exist_ok=True)
    
    try:
        # Create Windows placeholder
        print("🪟 Creating Windows placeholder...")
        windows_placeholder = os.path.join(public_dir, "Axora-Windows.exe")
        with open(windows_placeholder, "w") as f:
            f.write("Windows executable coming soon!")
        
        # Create macOS placeholder
        print("📱 Creating macOS placeholder...")
        macos_placeholder = os.path.join(public_dir, "Axora-macOS.zip")
        with open(macos_placeholder, "w") as f:
            f.write("macOS app coming soon!")
        
        # Copy website files to public directory
        print("📄 Copying website files...")
        files_to_copy = [
            "index.html",
            "QUICK_START.md",
            "INSTALLATION_GUIDE.md",
            "vercel.json"
        ]
        
        for file in files_to_copy:
            if os.path.exists(file):
                shutil.copy2(file, public_dir)
        
        print("✅ Vercel build completed successfully!")
        print(f"📁 Files ready in: {public_dir}/")
        print("\n🚀 Next steps:")
        print("1. Go to https://vercel.com")
        print("2. Sign up/Login with GitHub")
        print("3. Click 'New Project'")
        print("4. Import your GitHub repository")
        print("5. Deploy!")
        print("\n🌐 Your site will be available at: https://axora.vercel.app")
        
        return True
        
    except Exception as e:
        print(f"❌ Error building for Vercel: {e}")
        return False

if __name__ == "__main__":
    build_for_vercel_simple()

