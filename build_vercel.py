#!/usr/bin/env python3
"""
Build Axora for Vercel deployment
"""
import os
import shutil
import subprocess
import sys

def build_for_vercel():
    """Build Axora for Vercel deployment"""
    print("🚀 Building Axora for Vercel deployment...")
    
    # Create public directory (Vercel's default)
    public_dir = "public"
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.makedirs(public_dir, exist_ok=True)
    
    try:
        # Build macOS app
        print("📱 Building macOS app...")
        subprocess.run([sys.executable, "build_macos.py"], check=True)
        
        # Create Windows placeholder
        print("🪟 Creating Windows placeholder...")
        windows_placeholder = os.path.join(public_dir, "Axora-Windows.exe")
        with open(windows_placeholder, "w") as f:
            f.write("Windows executable coming soon!")
        
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
        
        # Copy macOS app
        if os.path.exists("dist/Axora.app"):
            shutil.copytree("dist/Axora.app", os.path.join(public_dir, "Axora.app"))
        
        # Create zip for macOS
        print("📦 Creating macOS zip...")
        subprocess.run([
            "zip", "-r", 
            os.path.join(public_dir, "Axora-macOS.zip"), 
            "Axora.app"
        ], cwd=public_dir, check=True)
        
        # Remove the app directory (keep only zip)
        shutil.rmtree(os.path.join(public_dir, "Axora.app"))
        
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
    build_for_vercel()

