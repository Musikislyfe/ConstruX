# Voice Mode for Claude Code Desktop

Enable hands-free interaction with Claude Code using voice commands! This script adds speech-to-text and text-to-speech capabilities to Claude Code Desktop.

## Features

- **Speech-to-Text**: Speak your commands and questions to Claude Code
- **Text-to-Speech**: Hear Claude's responses read aloud
- **sounddevice Backend**: Uses sounddevice for reliable, cross-platform audio I/O (replaces PyAudio)
- **Hotkey Control**: Easy keyboard shortcuts for voice control
- **Push-to-Talk**: Hold a key to speak, release to send
- **Continuous Listening**: Hands-free mode with voice activation
- **Configurable**: Customize voice settings, hotkeys, and behavior
- **Cross-Platform**: Works on Linux, macOS, and Windows

## Requirements

- Python 3.7 or higher
- Working microphone
- Speakers or headphones
- Internet connection (for speech recognition)

## Installation

### Quick Install

#### Linux/macOS
```bash
chmod +x install_voice_mode.sh
./install_voice_mode.sh
```

#### Windows
```cmd
install_voice_mode.bat
```

### Manual Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install system dependencies:

**Linux (Ubuntu/Debian)**
```bash
sudo apt-get install libsndfile1 libportaudio2 xclip
```

**Linux (Fedora/RHEL)**
```bash
sudo yum install libsndfile portaudio xclip
```

**macOS**
```bash
brew install libsndfile portaudio
```

**Windows**
- sounddevice works out-of-the-box on Windows
- Ensure you have the latest Visual C++ Redistributable if you encounter issues

## Usage

### Basic Usage

Run voice mode:
```bash
python3 voice_mode.py
```

### Setup Wizard

Configure voice settings interactively:
```bash
python3 voice_mode.py --setup
```

### List Available Devices

Audio input devices:
```bash
python3 voice_mode.py --list-devices
```

TTS voices:
```bash
python3 voice_mode.py --list-voices
```

## Default Hotkeys

| Hotkey | Action |
|--------|--------|
| `Ctrl+Shift+V` | Toggle Voice Mode ON/OFF |
| `Ctrl+Space` | Push to Talk (hold to speak) |
| `Ctrl+Shift+S` | Stop Speaking (interrupt TTS) |

## How It Works

### Voice Input Flow

1. Press `Ctrl+Shift+V` to enable voice mode
2. Speak your command or question
3. The script converts speech to text using Google Speech Recognition
4. Text is copied to clipboard for pasting into Claude Code
5. Alternatively, text is written to `~/.claude_code_voice_input.txt`

### Voice Output Flow

1. Claude Code's responses can be read aloud
2. Text-to-speech is handled by pyttsx3 (offline TTS engine)
3. Adjust voice speed, volume, and voice type in config

## Configuration

Edit `voice_config.json` to customize settings:

### Speech Recognition Settings

```json
{
  "speech_recognition": {
    "language": "en-US",
    "energy_threshold": 4000,
    "pause_threshold": 0.8,
    "phrase_time_limit": 15
  }
}
```

- `language`: Language code (e.g., "en-US", "es-ES", "fr-FR")
- `energy_threshold`: Microphone sensitivity (lower = more sensitive)
- `pause_threshold`: Seconds of silence before stopping
- `phrase_time_limit`: Maximum recording time

### Text-to-Speech Settings

```json
{
  "text_to_speech": {
    "rate": 175,
    "volume": 0.9,
    "voice_id": 0
  }
}
```

- `rate`: Speaking speed (words per minute)
- `volume`: Volume level (0.0 to 1.0)
- `voice_id`: Voice selection (use --list-voices to see options)

### Hotkeys

```json
{
  "hotkeys": {
    "toggle_voice_mode": "ctrl+shift+v",
    "push_to_talk": "ctrl+space",
    "stop_speaking": "ctrl+shift+s"
  }
}
```

Customize keyboard shortcuts using standard key notation.

### Behavior Settings

```json
{
  "behavior": {
    "auto_speak_responses": true,
    "confirmation_sound": true,
    "show_transcript": true
  }
}
```

- `auto_speak_responses`: Automatically read responses aloud
- `confirmation_sound`: Play sound when toggling voice mode
- `show_transcript`: Display recognized text in console

## Integration with Claude Code

### Method 1: Clipboard Integration

The script copies recognized text to your system clipboard. Simply paste into Claude Code:

1. Voice mode recognizes your speech
2. Text is copied to clipboard
3. Paste (`Ctrl+V`) into Claude Code input

### Method 2: File Monitoring

The script writes input to `~/.claude_code_voice_input.txt`:

1. Configure Claude Code to monitor this file
2. Automatically process new voice commands
3. (Requires custom Claude Code configuration)

### Method 3: Direct Integration (Advanced)

For developers: Integrate directly with Claude Code's input API:

```python
from voice_mode import VoiceMode

voice = VoiceMode()
text = voice.listen()
# Send text to Claude Code's input handler
```

## Troubleshooting

### Microphone Not Working

1. Check microphone permissions in system settings
2. List available devices: `python3 voice_mode.py --list-devices`
3. Adjust `energy_threshold` in config (try 2000-6000)
4. Test microphone with: `python3 -m speech_recognition`

### Speech Recognition Errors

**"Could not understand audio"**
- Speak clearly and closer to microphone
- Reduce background noise
- Adjust `energy_threshold` lower
- Increase `pause_threshold`

**"Request Error"**
- Check internet connection (Google Speech Recognition requires internet)
- Consider offline alternative: Whisper (uncomment in requirements.txt)

### sounddevice Installation Issues

**Linux**: Install libsndfile and PortAudio
```bash
sudo apt-get install libsndfile1 libportaudio2
```

**macOS**: Install via Homebrew
```bash
brew install libsndfile portaudio
```

**Windows**: Usually works out-of-the-box
- If issues persist, ensure Visual C++ Redistributable is installed
- Check that audio drivers are up to date

### Hotkeys Not Working

**Linux**: May require running with sudo for global hotkeys
```bash
sudo python3 voice_mode.py
```

**macOS**: Grant accessibility permissions:
- System Preferences → Security & Privacy → Accessibility
- Add Terminal or your Python executable

**Windows**: Run as Administrator

### Text-to-Speech Issues

**No sound**
- Check volume settings in config
- Verify speakers/headphones are working
- List available voices: `python3 voice_mode.py --list-voices`

**Wrong voice**
- Change `voice_id` in config
- Use setup wizard to preview voices

## Advanced Usage

### Custom Wake Word

Enable wake word detection:

```json
{
  "behavior": {
    "wake_word_enabled": true,
    "wake_word": "hey claude"
  }
}
```

### Different Languages

```json
{
  "speech_recognition": {
    "language": "es-ES"
  }
}
```

Supported languages: en-US, en-GB, es-ES, fr-FR, de-DE, it-IT, pt-BR, ru-RU, ja-JP, zh-CN, and more.

### Offline Speech Recognition

For offline operation, install Whisper:

```bash
pip install openai-whisper torch
```

Modify voice_mode.py to use Whisper instead of Google Speech Recognition.

## Performance Tips

1. **Reduce latency**: Lower `pause_threshold` to 0.5-0.6
2. **Improve accuracy**: Speak clearly, reduce background noise
3. **Save bandwidth**: Use offline Whisper for speech recognition
4. **Faster TTS**: Increase `rate` to 200-250

## Why sounddevice?

This implementation uses **sounddevice** instead of PyAudio for several advantages:

- **Easier Installation**: No complex C dependencies or compilation issues
- **Better Cross-Platform Support**: Works out-of-the-box on Windows, easier on Linux/macOS
- **More Reliable**: Built on modern audio libraries (PortAudio + libsndfile)
- **Active Development**: Regular updates and better maintenance
- **Lower Latency**: More efficient audio processing

The migration from PyAudio to sounddevice maintains full compatibility with SpeechRecognition while providing a smoother installation experience.

## Privacy & Security

- Voice data is sent to Google Speech Recognition API
- For privacy, consider using offline Whisper
- No voice data is stored locally by default
- TTS is processed entirely offline (pyttsx3)

## Contributing

Improvements welcome! Some ideas:

- [ ] Add wake word detection
- [ ] Implement offline Whisper support
- [ ] Add voice activity detection (VAD)
- [ ] Support for multiple languages
- [ ] Custom command macros
- [ ] Integration with Claude Code's API

## License

MIT License - feel free to modify and distribute.

## Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check troubleshooting section above
- Review config settings in voice_config.json

---

**Happy voice coding with Claude! 🎤🤖**
