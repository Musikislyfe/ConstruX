@echo off
REM Installation script for Claude Code Voice Mode - Windows
REM Run this as Administrator for best results

echo ==================================================
echo   Claude Code Desktop - Voice Mode Installer
echo ==================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.7 or higher from python.org
    pause
    exit /b 1
)
echo [OK] Python found
echo.

echo Checking pip installation...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip not found. Installing pip...
    python -m ensurepip --default-pip
)
echo [OK] pip found
echo.

echo Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [WARNING] Some dependencies may have failed to install.
    echo If PyAudio failed, try:
    echo   1. pip install pipwin
    echo   2. pipwin install pyaudio
    echo Or download wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
    echo.
)

echo.
echo ==================================================
echo   Installation Complete!
echo ==================================================
echo.
echo To run voice mode:
echo   python voice_mode.py
echo.
echo To run setup wizard:
echo   python voice_mode.py --setup
echo.
echo ==================================================
echo   Default Hotkeys:
echo ==================================================
echo   Ctrl+Shift+V - Toggle Voice Mode
echo   Ctrl+Space   - Push to Talk
echo   Ctrl+Shift+S - Stop Speaking
echo ==================================================
echo.
pause
