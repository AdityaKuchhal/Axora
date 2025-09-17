# Utility Bill Organizer Pro - PyQt6 Version

A modern, professional desktop application for organizing utility bills by corporation, provider, and account.

## Features

- **Modern PyQt6 Interface**: Professional desktop application with clean, modern design
- **Smart File Organization**: Automatically organizes files by Corporation → Provider → Account → Year
- **3 Major Providers**: Bell, Rogers, Telus with proper case-sensitive folder naming
- **Account Folder Intelligence**: Supports both last 4 digits and 3-digit extensions
- **Year Organization**: Automatically organizes existing files by year before placing new files
- **Real-time Progress**: Live progress tracking with detailed status updates
- **Enhanced Date Recognition**: Multiple date pattern recognition for various file formats
- **Threaded Processing**: Non-blocking file organization with background processing

## Installation

1. **Install PyQt6 and dependencies**:

   ```bash
   pip install -r requirements_pyqt6.txt
   ```

2. **Run the application**:
   ```bash
   python utility_bill_organizer_pyqt6.py
   ```

## Usage

1. **Select Excel File**: Choose the Excel file containing corporation and account data
2. **Select Source Folder**: Choose the folder containing downloaded utility bill files
3. **Select Destination Folder**: Choose the Utilities folder where organized files will be saved
4. **Start Organization**: Click the "Start Organization" button to begin processing

## Organization Logic

- **If account folder is already organized by year** → Place file in correct year folder
- **If account folder has files directly** → Organize existing files by year first, then place new file

## Folder Structure

```
Utilities/
├── [Corp Number]/
│   ├── Bell/
│   ├── Rogers/
│   └── Telus/
│       └── [Account Folder]/
│           └── [Year]/
│               └── [YY-MM-DD files]
```

## Requirements

- Python 3.8+
- PyQt6
- pandas
- openpyxl

## Modern UI Features

- **Professional Design**: Clean, modern interface with proper spacing and typography
- **Responsive Layout**: Adapts to different window sizes with splitter panels
- **Real-time Feedback**: Live progress updates and status messages
- **Error Handling**: Comprehensive error reporting and user notifications
- **Threaded Processing**: Non-blocking UI during file operations
- **Modern Styling**: Custom CSS styling with hover effects and smooth transitions

## Differences from Tkinter Version

- **More Professional**: Native OS integration and professional appearance
- **Better Performance**: More efficient rendering and processing
- **Modern Widgets**: Rich set of modern UI components
- **Better Threading**: Proper background processing without UI freezing
- **Enhanced Styling**: More control over appearance and behavior



