# Axora Installation Guide

## 🍎 macOS Installation

### If you see "Axora is damaged and can't be opened"

This is a common macOS security feature. Here's how to fix it:

#### Method 1: Right-click and Open (Recommended)

1. **Right-click** on the `Axora.app` file
2. Select **"Open"** from the context menu
3. Click **"Open"** when macOS asks for confirmation
4. The app will now run normally

#### Method 2: System Preferences

1. Go to **System Preferences** → **Security & Privacy**
2. Click the **"General"** tab
3. Look for a message about Axora being blocked
4. Click **"Open Anyway"**
5. The app will now run normally

#### Method 3: Terminal Command (Advanced)

```bash
# Remove quarantine attributes
xattr -d com.apple.quarantine /path/to/Axora.app

# Or remove all extended attributes
xattr -cr /path/to/Axora.app
```

### Normal Installation

1. Download `Axora-macOS.zip`
2. Extract the zip file
3. Move `Axora.app` to your Applications folder
4. Double-click to run

## 🪟 Windows Installation

1. Download `Axora-Windows.exe`
2. Double-click to run
3. No additional installation required

## 🔧 Troubleshooting

### macOS Issues

- **"App can't be opened because it is from an unidentified developer"**
  - Use Method 1 above (Right-click → Open)
- **"App is damaged and can't be opened"**
  - Use Method 1 above (Right-click → Open)
  - Or try Method 3 (Terminal command)

### General Issues

- **App won't start**: Make sure you have the required system version
- **Excel file not found**: Place your Excel mapping file in the same folder as the app
- **Permission denied**: Check file permissions and try running as administrator (Windows)

## 📋 System Requirements

### macOS

- **Version**: macOS 10.15 (Catalina) or later
- **Architecture**: Intel or Apple Silicon (M1/M2)
- **Storage**: 500MB free space
- **Memory**: 4GB RAM recommended

### Windows

- **Version**: Windows 10 or later
- **Architecture**: 64-bit
- **Storage**: 500MB free space
- **Memory**: 4GB RAM recommended

## 🚀 First Run

1. **Select Excel File**: Choose your corporation/provider mapping file
2. **Choose Source Folder**: Select folder containing utility bills to organize
3. **Choose Destination**: Select your Utilities folder structure
4. **Click Execute**: Let Axora organize your files automatically

## 📞 Support

If you encounter any issues:

1. Check this installation guide
2. Verify system requirements
3. Try the troubleshooting steps above
4. Contact Aditya Kuchhal for support

---

**Built with ❤️ by Aditya Kuchhal**


