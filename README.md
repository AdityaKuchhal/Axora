# Axora - Utility Bill Organizer

A professional desktop application for organizing utility bills from Bell, Rogers, and Telus providers. Built with Python and PyQt6.

## Features

- 🗂️ **Smart File Organization**: Automatically organizes utility bills by corporation, provider, account number, and year
- 📅 **Year-based Structure**: Creates intelligent folder hierarchies with year-based organization
- 🏢 **Multi-Provider Support**: Handles Bell, Rogers, and Telus bills seamlessly
- 📊 **Excel Integration**: Uses Excel files to map account numbers to corporations and providers
- 🎨 **Modern UI**: Clean, responsive interface with dark/light theme support
- 📈 **Progress Tracking**: Real-time progress updates during file organization
- 📋 **History Logging**: Keeps track of all organization activities

## Installation

### Requirements

- Python 3.8 or later
- PyQt6
- pandas
- openpyxl

### Setup

```bash
# Clone the repository
git clone https://github.com/AdityaKuchhal/Axora.git
cd Axora

# Install dependencies
pip install -r requirements.txt

# Run the application
python axora.py
```

## Usage

1. **Prepare Excel File**: Create an Excel file with provider information (BELL, TELUS, ROGERS) in the first column, followed by corporation and account details
2. **Select Excel File**: Choose your Excel mapping file using the Browse button
3. **Select Source**: Choose either a single PDF file or a folder containing PDF files
4. **Choose Destination**: Select your Utilities folder where organized files will be placed
5. **Execute**: Click the Execute button to start the organization process
6. **Monitor Progress**: Watch the progress bar and results in real-time

## File Structure

The application organizes files in the following hierarchy:

```
Utilities/
├── [Corporation]/
│   ├── Bell/
│   │   └── [Account]/
│   │       ├── 2024/
│   │       ├── 2025/
│   │       └── [Organized Bills]
│   ├── Rogers/
│   │   └── [Account]/
│   └── Telus/
│       └── [Account]/
```

## How It Works

- **Account Extraction**: Extracts account identifiers (last 4 digits, extensions) from PDF filenames
- **Excel Mapping**: Matches extracted identifiers against Excel data to find corporation and provider
- **Date Extraction**: Extracts dates from filenames to organize by year
- **Smart Organization**: Creates organized folder structure and renames files chronologically

## Development

### Prerequisites

- Python 3.8+
- PyQt6
- pandas
- openpyxl

### Project Structure

```
Axora/
├── axora.py              # Main application file
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── LICENSE               # MIT License
└── builds/               # Build scripts
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Aditya Kuchhal**

- GitHub: [@AdityaKuchhal](https://github.com/AdityaKuchhal)

---

**Made with ❤️ by Aditya Kuchhal**
