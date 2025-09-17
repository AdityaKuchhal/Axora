# Axora Quick Start Guide

## 🚀 **Getting Started (macOS)**

### **Step 1: Download**

1. Download `Axora-macOS.zip` from the website
2. Extract the zip file
3. You'll see `Axora.app`

### **Step 2: Install (Important!)**

**⚠️ DO NOT double-click the app directly!**

Instead:

1. **Right-click** on `Axora.app`
2. Select **"Open"** from the context menu
3. Click **"Open"** when macOS asks for confirmation

### **Step 3: If You See "Damaged" Error**

This is normal macOS security behavior. Here's how to fix it:

#### **Method 1: Right-Click (Recommended)**

1. Right-click on `Axora.app`
2. Select "Open"
3. Click "Open" when prompted

#### **Method 2: System Preferences**

1. Go to **System Preferences** → **Security & Privacy**
2. Click **"General"** tab
3. Look for a message about Axora being blocked
4. Click **"Open Anyway"**

#### **Method 3: Terminal (Advanced)**

```bash
# Remove quarantine attributes
xattr -d com.apple.quarantine /path/to/Axora.app

# Or remove all extended attributes
xattr -cr /path/to/Axora.app
```

## 🪟 **Getting Started (Windows)**

### **Step 1: Download**

1. Download `Axora-Windows.exe` from the website
2. Save it to your desired location

### **Step 2: Run**

1. Double-click `Axora-Windows.exe`
2. No installation required!

## 📋 **First Use**

1. **Select Excel File**: Choose your corporation/provider mapping file
2. **Choose Source Folder**: Select folder containing utility bills
3. **Choose Destination**: Select your Utilities folder
4. **Click Execute**: Let Axora organize your files!

## 🔧 **Troubleshooting**

### **macOS Issues**

- **"App can't be opened"**: Use right-click method above
- **"App is damaged"**: Use right-click method above
- **Permission denied**: Check file permissions

### **Windows Issues**

- **Antivirus blocking**: Add exception for Axora.exe
- **Missing dependencies**: Download Visual C++ Redistributable
- **App won't start**: Run as administrator

## 📞 **Need Help?**

Contact **Aditya Kuchhal** for support:

- Technical issues
- Custom requirements
- Priority Windows access

---

**Built with ❤️ by Aditya Kuchhal**


