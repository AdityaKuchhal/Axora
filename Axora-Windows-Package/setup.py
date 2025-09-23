import sys
import subprocess
import os

def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def main():
    print("Axora - Utility Bill Organizer")
    print("Installing dependencies...")
    
    if install_requirements():
        print("\n🎉 Setup complete! You can now run axora.py")
    else:
        print("\n❌ Setup failed. Please install dependencies manually:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()
