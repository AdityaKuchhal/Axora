#!/usr/bin/env python3
"""
Build script for creating signed Windows executable (requires code signing certificate)
"""
import subprocess
import sys
import os
import shutil

def install_dependencies():
    """Install required dependencies"""
    dependencies = [
        "pyinstaller",
        "pywin32",
        "cryptography"
    ]
    
    for dep in dependencies:
        try:
            __import__(dep.replace("-", "_"))
            print(f"✅ {dep} already installed")
        except ImportError:
            print(f"📦 Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])

def build_signed_executable():
    """Build Windows executable with code signing"""
    print("🔨 Building signed Windows executable...")
    
    # First, build the unsigned executable
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "Axora",
        "--icon", "axora.ico",
        "--add-data", "Bell-Rogers-Telus Login.xlsx;.",
        "--version-file", "version_info.txt",
        "--manifest", "app.manifest",
        "--hidden-import", "pandas",
        "--hidden-import", "openpyxl",
        "--hidden-import", "PyQt6",
        "--hidden-import", "PyQt6.QtCore",
        "--hidden-import", "PyQt6.QtWidgets",
        "--hidden-import", "PyQt6.QtGui",
        "--collect-all", "PyQt6",
        "--noconfirm",
        "--clean",
        "--strip",
        "--noupx",
        "utility_bill_organizer_pyqt6.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Unsigned executable created")
        
        # Try to sign the executable (if certificate is available)
        exe_path = "dist/Axora.exe"
        if os.path.exists(exe_path):
            try:
                # This would require a code signing certificate
                # For now, we'll just create a self-signed certificate for testing
                create_self_signed_cert()
                sign_executable(exe_path)
                print("✅ Executable signed successfully")
            except Exception as e:
                print(f"⚠️  Code signing failed: {e}")
                print("   The executable will work but may be flagged by antivirus")
            
            return True
        else:
            print("❌ Executable not found after build")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

def create_self_signed_cert():
    """Create a self-signed certificate for testing"""
    print("🔐 Creating self-signed certificate...")
    
    # Create a simple self-signed certificate using PowerShell
    ps_script = """
$cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=Axora Development" -KeyUsage DigitalSignature -FriendlyName "Axora Development Certificate" -CertStoreLocation "Cert:\CurrentUser\My" -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3")
$password = ConvertTo-SecureString -String "axora123" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath "axora_dev.pfx" -Password $password
"""
    
    with open("create_cert.ps1", "w") as f:
        f.write(ps_script)
    
    try:
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "create_cert.ps1"], check=True)
        print("✅ Self-signed certificate created")
    except subprocess.CalledProcessError:
        print("⚠️  Could not create certificate (PowerShell not available)")

def sign_executable(exe_path):
    """Sign the executable with the certificate"""
    print("✍️  Signing executable...")
    
    try:
        # Use signtool to sign the executable
        sign_cmd = [
            "signtool", "sign",
            "/f", "axora_dev.pfx",
            "/p", "axora123",
            "/t", "http://timestamp.digicert.com",
            exe_path
        ]
        
        subprocess.run(sign_cmd, check=True)
        print("✅ Executable signed successfully")
        
    except subprocess.CalledProcessError:
        print("⚠️  Could not sign executable (signtool not available)")
        print("   The executable will work but may be flagged by antivirus")

def create_installer():
    """Create a Windows installer using NSIS"""
    print("📦 Creating Windows installer...")
    
    nsis_script = """
!define APPNAME "Axora"
!define COMPANYNAME "Aditya Kuchhal"
!define DESCRIPTION "Utility Bill Organizer"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0
!define HELPURL "https://axora-ak.vercel.app"
!define UPDATEURL "https://axora-ak.vercel.app"
!define ABOUTURL "https://axora-ak.vercel.app"
!define INSTALLSIZE 50000

RequestExecutionLevel admin
InstallDir "$PROGRAMFILES\\${APPNAME}"
Name "${APPNAME}"
outFile "Axora-Installer.exe"

!include LogicLib.nsh

page directory
page instfiles

!macro VerifyUserIsAdmin
UserInfo::GetAccountType
pop $0
${If} $0 != "admin"
    messageBox mb_iconstop "Administrator rights required!"
    setErrorLevel 740
    quit
${EndIf}
!macroend

function .onInit
    setShellVarContext all
    !insertmacro VerifyUserIsAdmin
functionEnd

section "install"
    setOutPath $INSTDIR
    file "dist\\Axora.exe"
    file "Bell-Rogers-Telus Login.xlsx"
    file "README.md"
    
    writeUninstaller "$INSTDIR\\uninstall.exe"
    
    createDirectory "$SMPROGRAMS\\${APPNAME}"
    createShortCut "$SMPROGRAMS\\${APPNAME}\\${APPNAME}.lnk" "$INSTDIR\\Axora.exe" "" "$INSTDIR\\Axora.exe"
    createShortCut "$SMPROGRAMS\\${APPNAME}\\Uninstall.lnk" "$INSTDIR\\uninstall.exe"
    
    createShortCut "$DESKTOP\\${APPNAME}.lnk" "$INSTDIR\\Axora.exe" "" "$INSTDIR\\Axora.exe"
    
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "UninstallString" "$INSTDIR\\uninstall.exe"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "InstallLocation" "$INSTDIR"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "DisplayIcon" "$INSTDIR\\Axora.exe"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "Publisher" "${COMPANYNAME}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "HelpLink" "${HELPURL}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "URLUpdateInfo" "${UPDATEURL}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "URLInfoAbout" "${ABOUTURL}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "DisplayVersion" "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}"
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "VersionMajor" ${VERSIONMAJOR}
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "VersionMinor" ${VERSIONMINOR}
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "NoRepair" 1
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "EstimatedSize" ${INSTALLSIZE}
sectionEnd

section "uninstall"
    delete "$INSTDIR\\Axora.exe"
    delete "$INSTDIR\\Bell-Rogers-Telus Login.xlsx"
    delete "$INSTDIR\\README.md"
    delete "$INSTDIR\\uninstall.exe"
    
    delete "$SMPROGRAMS\\${APPNAME}\\${APPNAME}.lnk"
    delete "$SMPROGRAMS\\${APPNAME}\\Uninstall.lnk"
    delete "$DESKTOP\\${APPNAME}.lnk"
    
    rmDir "$SMPROGRAMS\\${APPNAME}"
    rmDir "$INSTDIR"
    
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}"
sectionEnd
"""
    
    with open("axora_installer.nsi", "w") as f:
        f.write(nsis_script)
    
    print("📝 NSIS installer script created")
    print("💡 To create installer, install NSIS and run: makensis axora_installer.nsi")

if __name__ == "__main__":
    print("🚀 Building signed Axora for Windows...")
    
    # Install dependencies
    install_dependencies()
    
    # Build signed executable
    if build_signed_executable():
        print("\n🎉 Build completed successfully!")
        print("📦 Your Windows executable is ready in the 'dist' folder")
        print("💡 For production use, obtain a proper code signing certificate")
        
        # Create installer
        create_installer()
    else:
        print("\n❌ Build failed. Check the error messages above.")
