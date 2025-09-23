# Axora - Utility Bill Organizer for Windows

## Quick Installation

### Method 1: Automatic Installation (Recommended)
1. Double-click `install.bat`
2. Follow the on-screen instructions
3. Run `run-axora.bat` to start the application

### Method 2: PowerShell Installation
1. Right-click `install.ps1` and select "Run with PowerShell"
2. Follow the on-screen instructions
3. Run `run-axora.bat` to start the application

### Method 3: Manual Installation
1. Install Python 3.8+ from https://python.org
2. Open Command Prompt in this folder
3. Run: `pip install -r requirements.txt`
4. Run: `python axora.py`

## System Requirements
- Windows 10 or later
- Python 3.8 or later
- Internet connection (for initial setup)

## Features
- Modern, intuitive interface
- Automatic bill organization by corporation, provider, account, and year
- Smart account number detection
- Support for Bell, Rogers, and Telus providers
- Excel integration for account mapping

## Troubleshooting

### "Python is not recognized"
- Install Python from https://python.org
- Make sure to check "Add Python to PATH" during installation
- Restart your computer after installation

### "Module not found" errors
- Run `install.bat` to install required packages
- Or manually run: `pip install -r requirements.txt`

### Application won't start
- Make sure all files are in the same folder
- Check that `Bell-Rogers-Telus Login.xlsx` is present
- Try running as Administrator

### Windows Defender warnings
- This is normal for unsigned applications
- Click "More info" then "Run anyway"
- Or add the folder to Windows Defender exclusions

## File Structure
```
Axora-Windows-Package/
├── axora.py                    # Main application
├── axora.ico                   # Application icon
├── Bell-Rogers-Telus Login.xlsx # Account mapping file
├── requirements.txt            # Python dependencies
├── install.bat                 # Windows installer
├── install.ps1                 # PowerShell installer
├── run-axora.bat              # Application launcher
└── README.txt                 # This file
```

## Support
- Website: https://axora-ak.vercel.app
- GitHub: https://github.com/AdityaKuchhal/Axora

## License
MIT License - See LICENSE file for details

---
Created by Aditya Kuchhal
