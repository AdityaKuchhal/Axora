# Axora - Utility Bill Organizer

A modern, cross-platform desktop application for organizing utility bills from Bell, Rogers, and Telus providers. Built with Python and PyQt6.

![Axora Logo](axora.ico)

## Features

- 🗂️ **Smart File Organization**: Automatically organizes utility bills by corporation, provider, account number, and year
- 📅 **Year-based Structure**: Creates intelligent folder hierarchies with year-based organization
- 🏢 **Multi-Provider Support**: Handles Bell, Rogers, and Telus bills seamlessly
- 📊 **Excel Integration**: Uses Excel files to map account numbers to corporations and providers
- 🎨 **Modern UI**: Clean, responsive interface with dark/light theme support
- 📱 **Cross-Platform**: Works on macOS and Windows
- 📈 **Progress Tracking**: Real-time progress updates during file organization
- 📋 **History Logging**: Keeps track of all organization activities

## Installation

### macOS
1. Download `Axora-macOS.zip` from the [Releases](https://github.com/AdityaKuchhal/Axora/releases) page
2. Extract the zip file
3. Move `Axora.app` to your Applications folder
4. Right-click and select "Open" to bypass macOS security warnings
5. Follow the on-screen instructions

### Windows
1. Download `Axora-Windows.exe` from the [Releases](https://github.com/AdityaKuchhal/Axora/releases) page
2. Double-click to run (no installation required)
3. Follow the on-screen instructions

## Usage

1. **Prepare Excel File**: Create an Excel file with columns for Corporation, Account Number, and Provider
2. **Select Files**: Choose your Excel mapping file and source folder containing utility bills
3. **Choose Destination**: Select your Utilities folder where organized files will be placed
4. **Execute**: Click the Execute button to start the organization process
5. **Monitor Progress**: Watch the progress bar and results in real-time

## File Structure

The application organizes files in the following hierarchy:

```
Utilities/
├── [Corporation Number]/
│   ├── Bell/
│   │   └── [Account Folder]/
│   │       ├── 2024/
│   │       ├── 2025/
│   │       └── [Latest Bill]
│   ├── Rogers/
│   │   └── [Account Folder]/
│   └── Telus/
│       └── [Account Folder]/
```

## Requirements

- **macOS**: 10.15 or later
- **Windows**: Windows 10 or later
- **Excel File**: Must contain Corporation, Account Number, and Provider columns

## Development

### Prerequisites
- Python 3.11+
- PyQt6
- pandas
- openpyxl
- PyInstaller

### Setup
```bash
# Clone the repository
git clone https://github.com/AdityaKuchhal/Axora.git
cd Axora

# Install dependencies
pip install -r requirements_pyqt6.txt

# Run the application
python utility_bill_organizer_pyqt6.py
```

### Building Executables

#### macOS
```bash
python build_macos.py
```

#### Windows
```bash
python build_windows.py
```

#### Both Platforms
```bash
python build_all.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Aditya Kuchhal**
- GitHub: [@AdityaKuchhal](https://github.com/AdityaKuchhal)
- Email: [Your Email]

## Acknowledgments

- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- Icons and UI inspired by modern design principles
- Special thanks to the Python community for excellent libraries

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/AdityaKuchhal/Axora/issues) page
2. Create a new issue with detailed information
3. Contact the author directly

---

**Made with ❤️ by Aditya Kuchhal**
