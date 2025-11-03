@echo off
setlocal

echo === Axora Windows Build ===
echo Installing dependencies...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt || goto :error

echo Cleaning previous build artifacts...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist Axora.spec del /f /q Axora.spec

echo Building executable with PyInstaller...
pyinstaller --noconfirm --clean --windowed ^
  --name "Axora" ^
  --icon "axora.ico" ^
  --add-data "axora.ico;." ^
  --collect-all PyQt6 ^
  --collect-all pandas ^
  --collect-data pandas ^
  --onefile utility_bill_organizer_pyqt6.py || goto :error

echo.
echo Build complete. Output: dist\Axora.exe
exit /b 0

:error
echo.
echo Build failed. Check the output above for details.
exit /b 1

endlocal

