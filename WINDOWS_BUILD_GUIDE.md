# Windows Build Guide for Axora

## 🪟 Building Windows Executable

Since we're currently on macOS, we need to build the Windows executable on a Windows machine. Here's the complete guide:

### **Prerequisites on Windows Machine:**

1. **Python 3.11+** installed
2. **Git** (to clone the repository)
3. **Windows 10/11** (64-bit recommended)

### **Step 1: Clone the Repository**

```bash
git clone <your-repository-url>
cd Axora
```

### **Step 2: Install Dependencies**

```bash
pip install -r requirements_pyqt6.txt
pip install pyinstaller
```

### **Step 3: Build Windows Executable**

```bash
python build_windows.py
```

### **Step 4: Test the Executable**

```bash
# The executable will be created in dist/Axora.exe
# Double-click to test, or run from command line:
dist\Axora.exe
```

## 🔧 **Alternative: Automated Build Script**

Create this script on Windows:

```python
# build_windows_automated.py
import subprocess
import sys
import os

def build_windows():
    """Build Windows executable with all dependencies"""

    # Install dependencies
    print("📦 Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "pandas", "openpyxl", "PyQt6"])

    # Build executable
    print("🔨 Building Windows executable...")
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "Axora",
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
        print("📁 Output: dist/Axora.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

if __name__ == "__main__":
    build_windows()
```

## 📋 **Expected Output**

After successful build:

- **File**: `dist/Axora.exe`
- **Size**: ~200-300MB (includes all dependencies)
- **Type**: Standalone executable (no installation needed)
- **Compatibility**: Windows 10/11 (64-bit)

## 🚀 **Deployment**

1. **Test locally** on Windows machine
2. **Upload to website** (replace placeholder)
3. **Update download links** on website
4. **Test download** from website

## 🔍 **Troubleshooting**

### Common Issues:

- **Missing dependencies**: Run `pip install -r requirements_pyqt6.txt`
- **PyQt6 not found**: Install with `pip install PyQt6`
- **Excel file not found**: Ensure `Bell-Rogers-Telus Login.xlsx` is in the same directory
- **Antivirus blocking**: Add exception for the executable

### Build Errors:

- **Import errors**: Add missing modules to `--hidden-import`
- **File not found**: Check file paths and permissions
- **Memory issues**: Close other applications during build

## 📞 **Support**

If you encounter issues:

1. Check this guide
2. Verify all prerequisites
3. Try the automated build script
4. Contact Aditya Kuchhal for support

---

**Note**: This guide assumes you have access to a Windows machine. If not, consider using:

- **Virtual Machine** (VMware, VirtualBox)
- **Cloud Windows instance** (AWS, Azure, Google Cloud)
- **GitHub Actions** (automated Windows build)


