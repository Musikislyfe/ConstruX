#!/bin/bash
# Installation script for Claude Code Voice Mode
# Supports Linux, macOS, and Windows (via Git Bash)

set -e

echo "=================================================="
echo "  Claude Code Desktop - Voice Mode Installer"
echo "=================================================="
echo ""

# Detect OS
OS="$(uname -s)"
case "$OS" in
    Linux*)     PLATFORM=Linux;;
    Darwin*)    PLATFORM=macOS;;
    MINGW*|MSYS*|CYGWIN*)    PLATFORM=Windows;;
    *)          PLATFORM="UNKNOWN:${OS}";;
esac

echo "Detected platform: $PLATFORM"
echo ""

# Check Python installation
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    echo "✓ Python 3 found: $(python3 --version)"
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
    echo "✓ Python found: $(python --version)"
else
    echo "✗ Python not found. Please install Python 3.7 or higher."
    exit 1
fi

# Check pip installation
echo "Checking pip installation..."
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo "✗ pip not found. Installing pip..."
    $PYTHON_CMD -m ensurepip --default-pip
fi
echo "✓ pip found"
echo ""

# Install platform-specific dependencies
echo "Installing platform-specific dependencies..."
if [ "$PLATFORM" = "Linux" ]; then
    echo "Linux detected. Installing system dependencies..."

    if command -v apt-get &> /dev/null; then
        echo "Using apt-get..."
        sudo apt-get update
        sudo apt-get install -y python3-pyaudio portaudio19-dev xclip
    elif command -v yum &> /dev/null; then
        echo "Using yum..."
        sudo yum install -y python3-pyaudio portaudio-devel xclip
    elif command -v pacman &> /dev/null; then
        echo "Using pacman..."
        sudo pacman -S --noconfirm python-pyaudio portaudio xclip
    else
        echo "⚠️  Could not detect package manager. Please install:"
        echo "   - portaudio (for PyAudio)"
        echo "   - xclip (for clipboard support)"
    fi

elif [ "$PLATFORM" = "macOS" ]; then
    echo "macOS detected. Installing system dependencies..."

    if command -v brew &> /dev/null; then
        echo "Using Homebrew..."
        brew install portaudio
    else
        echo "⚠️  Homebrew not found. Please install Homebrew first:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        echo "   Then run: brew install portaudio"
    fi

elif [ "$PLATFORM" = "Windows" ]; then
    echo "Windows detected."
    echo "⚠️  On Windows, you may need to install PyAudio manually:"
    echo "   Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio"
    echo "   Or use: pip install pipwin && pipwin install pyaudio"
fi

echo ""

# Create virtual environment (optional but recommended)
echo "Would you like to create a virtual environment? (recommended) [y/N]"
read -r CREATE_VENV

if [[ $CREATE_VENV =~ ^[Yy]$ ]]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv_voice_mode

    if [ "$PLATFORM" = "Windows" ]; then
        source venv_voice_mode/Scripts/activate
    else
        source venv_voice_mode/bin/activate
    fi

    echo "✓ Virtual environment created and activated"
else
    echo "Skipping virtual environment creation"
fi

echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
$PYTHON_CMD -m pip install --upgrade pip
$PYTHON_CMD -m pip install -r requirements.txt

echo ""
echo "✓ Python dependencies installed"
echo ""

# Make voice_mode.py executable
chmod +x voice_mode.py

echo "=================================================="
echo "  Installation Complete!"
echo "=================================================="
echo ""
echo "To run voice mode:"
echo "  python3 voice_mode.py"
echo ""
echo "To run setup wizard:"
echo "  python3 voice_mode.py --setup"
echo ""
echo "To list available audio devices:"
echo "  python3 voice_mode.py --list-devices"
echo ""
echo "To list available voices:"
echo "  python3 voice_mode.py --list-voices"
echo ""

if [[ $CREATE_VENV =~ ^[Yy]$ ]]; then
    echo "Note: Virtual environment created. To activate it:"
    if [ "$PLATFORM" = "Windows" ]; then
        echo "  venv_voice_mode\\Scripts\\activate"
    else
        echo "  source venv_voice_mode/bin/activate"
    fi
    echo ""
fi

echo "=================================================="
echo "  Default Hotkeys:"
echo "=================================================="
echo "  Ctrl+Shift+V - Toggle Voice Mode"
echo "  Ctrl+Space   - Push to Talk"
echo "  Ctrl+Shift+S - Stop Speaking"
echo "=================================================="
