@echo off
title Axora Installer
echo.
echo ========================================
echo    Axora - Utility Bill Organizer
echo ========================================
echo.
echo Installing Axora...
echo.

REM Create desktop shortcut
echo Creating desktop shortcut...
if exist "Axora-Windows.exe" (
    echo [InternetShortcut] > "%USERPROFILE%\Desktop\Axora.url"
    echo URL=file:///%CD%\Axora-Windows.exe >> "%USERPROFILE%\Desktop\Axora.url"
    echo IconFile=%CD%\Axora-Windows.exe >> "%USERPROFILE%\Desktop\Axora.url"
    echo IconIndex=0 >> "%USERPROFILE%\Desktop\Axora.url"
) else (
    echo [InternetShortcut] > "%USERPROFILE%\Desktop\Axora.url"
    echo URL=file:///%CD%\Axora-Windows.bat >> "%USERPROFILE%\Desktop\Axora.url"
    echo IconFile=%CD%\Axora-Windows.bat >> "%USERPROFILE%\Desktop\Axora.url"
    echo IconIndex=0 >> "%USERPROFILE%\Desktop\Axora.url"
)

echo.
echo ✅ Installation completed!
echo.
echo You can now run Axora from your desktop or this folder.
echo.
pause
