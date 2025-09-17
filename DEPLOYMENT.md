# Axora Deployment Guide

## 🚀 Quick Start

### Option 1: Local Testing

```bash
# Test the website locally
python3 deploy_website.py
# Opens http://localhost:8000 in your browser
```

### Option 2: Build Everything

```bash
# Build executables and website
python3 build_all.py
```

## 📦 What Gets Created

### Executables

- **macOS**: `dist/Axora.app` (430MB) - Native macOS application
- **Windows**: `dist/Axora.exe` (when built on Windows)

### Website Files

- **`downloads/index.html`** - Beautiful landing page
- **`downloads/Axora-macOS.zip`** - macOS download (430MB)
- **`downloads/Axora-Windows.exe`** - Windows download (when available)
- **`downloads/README.txt`** - Installation instructions

## 🌐 Website Deployment Options

### Option 1: GitHub Pages (Free)

1. Create a GitHub repository
2. Upload the `downloads` folder contents to the repository
3. Enable GitHub Pages in repository settings
4. Your website will be available at `https://yourusername.github.io/repositoryname`

### Option 2: Netlify (Free)

1. Go to [netlify.com](https://netlify.com)
2. Drag and drop the `downloads` folder
3. Your website will be live instantly

### Option 3: Vercel (Free)

1. Go to [vercel.com](https://vercel.com)
2. Connect your GitHub repository
3. Deploy automatically

### Option 4: Custom Server

1. Upload the `downloads` folder to your web server
2. Ensure the executable files are accessible
3. Update download links in `index.html` if needed

## 🔧 Customization

### Website Styling

Edit `index.html` to customize:

- Colors and fonts
- Logo and branding
- Feature descriptions
- Download buttons

### App Information

Update in `utility_bill_organizer_pyqt6.py`:

- App name and version
- About dialog content
- Window title

## 📱 Features Included

### Website

- ✅ Responsive design (mobile-friendly)
- ✅ Modern UI with gradients and animations
- ✅ Download buttons for both platforms
- ✅ System requirements
- ✅ Feature list
- ✅ Professional styling

### Executables

- ✅ Single-file executables (no installation needed)
- ✅ All dependencies included
- ✅ Excel file bundled
- ✅ Cross-platform support
- ✅ Native app bundles (.app for macOS)

## 🛠️ Build Process

The `build_all.py` script:

1. Installs PyInstaller and dependencies
2. Builds macOS app bundle
3. Creates proper .app structure
4. Packages everything for download
5. Generates website files
6. Cleans up build artifacts

## 📋 File Structure After Build

```
Axora/
├── utility_bill_organizer_pyqt6.py    # Source code
├── build_all.py                       # Build script
├── deploy_website.py                  # Local testing
├── index.html                         # Website template
├── downloads/                         # Ready for deployment
│   ├── index.html                     # Website
│   ├── Axora-macOS.zip               # macOS download
│   ├── Axora-Windows.exe             # Windows download
│   └── README.txt                     # Instructions
├── dist/                              # Build output
│   └── Axora.app                     # macOS app bundle
└── Utilities/                         # Sample organized structure
```

## 🎯 Next Steps

1. **Test locally**: Run `python3 deploy_website.py`
2. **Choose deployment**: Pick GitHub Pages, Netlify, or custom server
3. **Upload files**: Deploy the `downloads` folder
4. **Share your app**: Users can download and run immediately!

## 💡 Tips

- The macOS app is large (430MB) due to all dependencies being included
- Windows executable will be smaller when built on Windows
- Consider using a CDN for faster downloads
- Add analytics to track downloads
- Update version numbers in both app and website

---

**Ready to deploy?** Just run `python3 build_all.py` and upload the `downloads` folder! 🚀



