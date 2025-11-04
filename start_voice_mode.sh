#!/bin/bash
# Quick start script for Claude Code Voice Mode

echo "Starting Claude Code Voice Mode..."

# Check if virtual environment exists
if [ -d "venv_voice_mode" ]; then
    source venv_voice_mode/bin/activate
    echo "Virtual environment activated"
fi

# Run voice mode
python3 voice_mode.py "$@"
