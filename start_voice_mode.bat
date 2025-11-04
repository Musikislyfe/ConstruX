@echo off
REM Quick start script for Claude Code Voice Mode - Windows

echo Starting Claude Code Voice Mode...

REM Check if virtual environment exists
if exist venv_voice_mode\Scripts\activate.bat (
    call venv_voice_mode\Scripts\activate.bat
    echo Virtual environment activated
)

REM Run voice mode
python voice_mode.py %*
