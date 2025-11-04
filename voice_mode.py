#!/usr/bin/env python3
"""
Voice Mode for Claude Code Desktop
Enables speech-to-text input and text-to-speech output for Claude Code

Features:
- Real-time speech recognition
- Natural text-to-speech output
- Hotkey activation/deactivation
- Multiple voice engines support
- Configurable settings
"""

import speech_recognition as sr
import pyttsx3
import pyaudio
import json
import os
import sys
import threading
import queue
import time
from pathlib import Path
import keyboard
import subprocess
import platform

class VoiceMode:
    def __init__(self, config_path="voice_config.json"):
        """Initialize Voice Mode with configuration"""
        self.config_path = config_path
        self.config = self.load_config()

        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.configure_tts()

        # Voice mode state
        self.is_listening = False
        self.is_speaking = False
        self.voice_enabled = False

        # Queue for managing speech output
        self.speech_queue = queue.Queue()

        # Adjust for ambient noise
        print("Calibrating microphone for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Microphone calibrated!")

    def load_config(self):
        """Load configuration from JSON file"""
        default_config = {
            "speech_recognition": {
                "language": "en-US",
                "energy_threshold": 4000,
                "pause_threshold": 0.8,
                "phrase_time_limit": 15
            },
            "text_to_speech": {
                "rate": 175,
                "volume": 0.9,
                "voice_id": 0
            },
            "hotkeys": {
                "toggle_voice_mode": "ctrl+shift+v",
                "push_to_talk": "ctrl+space",
                "stop_speaking": "ctrl+shift+s"
            },
            "behavior": {
                "auto_speak_responses": True,
                "confirmation_sound": True,
                "show_transcript": True
            }
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults
                    default_config.update(loaded_config)
            except Exception as e:
                print(f"Error loading config: {e}")
        else:
            # Save default config
            self.save_config(default_config)

        return default_config

    def save_config(self, config=None):
        """Save configuration to JSON file"""
        if config is None:
            config = self.config

        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)

    def configure_tts(self):
        """Configure text-to-speech engine"""
        tts_config = self.config["text_to_speech"]

        self.tts_engine.setProperty('rate', tts_config["rate"])
        self.tts_engine.setProperty('volume', tts_config["volume"])

        # Set voice
        voices = self.tts_engine.getProperty('voices')
        if voices and tts_config["voice_id"] < len(voices):
            self.tts_engine.setProperty('voice', voices[tts_config["voice_id"]].id)

    def speak(self, text):
        """Convert text to speech"""
        if not text or not self.config["behavior"]["auto_speak_responses"]:
            return

        self.is_speaking = True
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
        finally:
            self.is_speaking = False

    def listen(self, timeout=None, phrase_time_limit=None):
        """Listen for voice input and convert to text"""
        if phrase_time_limit is None:
            phrase_time_limit = self.config["speech_recognition"]["phrase_time_limit"]

        try:
            with self.microphone as source:
                print("\n🎤 Listening...")
                self.is_listening = True

                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

                self.is_listening = False
                print("🔄 Processing speech...")

                # Recognize speech using Google Speech Recognition
                text = self.recognizer.recognize_google(
                    audio,
                    language=self.config["speech_recognition"]["language"]
                )

                if self.config["behavior"]["show_transcript"]:
                    print(f"📝 Transcript: {text}")

                return text

        except sr.WaitTimeoutError:
            print("⏱️  No speech detected")
            return None
        except sr.UnknownValueError:
            print("❓ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
        finally:
            self.is_listening = False

    def toggle_voice_mode(self):
        """Toggle voice mode on/off"""
        self.voice_enabled = not self.voice_enabled
        status = "ENABLED" if self.voice_enabled else "DISABLED"
        print(f"\n🔊 Voice Mode {status}")

        if self.config["behavior"]["confirmation_sound"]:
            message = f"Voice mode {status.lower()}"
            threading.Thread(target=self.speak, args=(message,), daemon=True).start()

    def stop_speaking(self):
        """Stop current speech output"""
        try:
            self.tts_engine.stop()
            self.is_speaking = False
            print("🔇 Speech stopped")
        except Exception as e:
            print(f"Error stopping speech: {e}")

    def continuous_listening_mode(self):
        """Continuous listening mode for hands-free operation"""
        print("\n🎯 Continuous Listening Mode")
        print("Say 'stop listening' to exit")

        while self.voice_enabled:
            text = self.listen(timeout=5)

            if text:
                if "stop listening" in text.lower():
                    print("👋 Exiting continuous mode")
                    break

                # Send text to Claude Code (this would integrate with Claude Code's input)
                self.process_voice_command(text)

            time.sleep(0.1)

    def process_voice_command(self, text):
        """Process voice command and send to Claude Code"""
        print(f"\n💬 Command: {text}")

        # Here you would integrate with Claude Code's input mechanism
        # For now, we'll simulate by writing to a file that Claude Code could monitor
        self.send_to_claude_code(text)

    def send_to_claude_code(self, text):
        """Send text to Claude Code desktop application"""
        # Method 1: Write to a temporary file that Claude Code monitors
        temp_file = Path.home() / ".claude_code_voice_input.txt"
        with open(temp_file, 'w') as f:
            f.write(text)

        # Method 2: Use clipboard (cross-platform)
        try:
            if platform.system() == "Darwin":  # macOS
                subprocess.run(['pbcopy'], input=text.encode('utf-8'), check=True)
            elif platform.system() == "Linux":
                subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode('utf-8'), check=True)
            elif platform.system() == "Windows":
                subprocess.run(['clip'], input=text.encode('utf-8'), check=True)
            print("📋 Text copied to clipboard - paste into Claude Code")
        except Exception as e:
            print(f"Clipboard error: {e}")

    def push_to_talk_mode(self):
        """Single voice input with push-to-talk"""
        print("\n🎤 Push-to-talk mode")
        text = self.listen()

        if text:
            self.process_voice_command(text)
            return text
        return None

    def setup_hotkeys(self):
        """Setup keyboard hotkeys for voice mode control"""
        hotkeys = self.config["hotkeys"]

        try:
            # Toggle voice mode
            keyboard.add_hotkey(
                hotkeys["toggle_voice_mode"],
                self.toggle_voice_mode
            )
            print(f"✅ Hotkey registered: {hotkeys['toggle_voice_mode']} - Toggle Voice Mode")

            # Push to talk
            keyboard.add_hotkey(
                hotkeys["push_to_talk"],
                self.push_to_talk_mode
            )
            print(f"✅ Hotkey registered: {hotkeys['push_to_talk']} - Push to Talk")

            # Stop speaking
            keyboard.add_hotkey(
                hotkeys["stop_speaking"],
                self.stop_speaking
            )
            print(f"✅ Hotkey registered: {hotkeys['stop_speaking']} - Stop Speaking")

        except Exception as e:
            print(f"⚠️  Error setting up hotkeys: {e}")

    def list_audio_devices(self):
        """List available audio input devices"""
        print("\n🎤 Available Audio Devices:")
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"  [{index}] {name}")

    def list_voices(self):
        """List available TTS voices"""
        print("\n🔊 Available TTS Voices:")
        voices = self.tts_engine.getProperty('voices')
        for index, voice in enumerate(voices):
            print(f"  [{index}] {voice.name} ({voice.id})")

    def interactive_setup(self):
        """Interactive setup wizard for voice mode"""
        print("\n" + "="*60)
        print("🎙️  CLAUDE CODE VOICE MODE - INTERACTIVE SETUP")
        print("="*60)

        # Show available devices
        self.list_audio_devices()
        self.list_voices()

        print("\n" + "="*60)
        print("Setup complete! Voice mode is ready.")
        print("="*60)

    def run(self):
        """Run the voice mode application"""
        print("\n" + "="*60)
        print("🎙️  CLAUDE CODE DESKTOP - VOICE MODE")
        print("="*60)
        print(f"\nHotkeys:")
        print(f"  {self.config['hotkeys']['toggle_voice_mode']} - Toggle Voice Mode")
        print(f"  {self.config['hotkeys']['push_to_talk']} - Push to Talk")
        print(f"  {self.config['hotkeys']['stop_speaking']} - Stop Speaking")
        print(f"\nPress Ctrl+C to exit")
        print("="*60)

        # Setup hotkeys
        self.setup_hotkeys()

        # Welcome message
        threading.Thread(
            target=self.speak,
            args=("Voice mode initialized. Press Control Shift V to enable voice mode.",),
            daemon=True
        ).start()

        try:
            # Keep the program running
            while True:
                if self.voice_enabled:
                    self.continuous_listening_mode()
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down voice mode...")
            self.speak("Voice mode shutting down")
            sys.exit(0)

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Voice Mode for Claude Code Desktop")
    parser.add_argument('--setup', action='store_true', help='Run interactive setup')
    parser.add_argument('--list-devices', action='store_true', help='List audio devices')
    parser.add_argument('--list-voices', action='store_true', help='List TTS voices')
    parser.add_argument('--config', default='voice_config.json', help='Config file path')

    args = parser.parse_args()

    voice_mode = VoiceMode(config_path=args.config)

    if args.list_devices:
        voice_mode.list_audio_devices()
        return

    if args.list_voices:
        voice_mode.list_voices()
        return

    if args.setup:
        voice_mode.interactive_setup()
        return

    # Run voice mode
    voice_mode.run()

if __name__ == "__main__":
    main()
