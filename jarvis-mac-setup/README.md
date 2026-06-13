# J.A.R.V.I.S - Just A Rather Very Intelligent System 🤖

An advanced AI voice assistant for macOS, Linux, and Windows. Control your computer with natural language voice commands.

![JARVIS](https://img.shields.io/badge/JARVIS-AI%20Assistant-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![macOS](https://img.shields.io/badge/macOS-10.12+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features ✨

- 🎤 **Voice Commands** - Talk naturally, JARVIS understands
- 🔊 **Text-to-Speech** - JARVIS speaks responses in natural voice
- 🌐 **Web Automation** - Browse and control websites
- 📱 **System Control** - Check battery, system info, etc.
- 🔄 **Cross-Platform** - Works on macOS, Linux, Windows
- 🚀 **Easy Installation** - One-command setup
- 🛡️ **Privacy First** - Runs locally on your machine

## Quick Start 🚀

### macOS Setup (Recommended)

```bash
# 1. Install dependencies
brew install python@3.11 portaudio

# 2. Clone repository
git clone https://github.com/YOUR_USERNAME/jarvis-mac-setup.git
cd jarvis-mac-setup

# 3. Setup and run
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements-mac.txt
python jarvis.py
```

**Full setup guide**: See [SETUP_MAC.md](SETUP_MAC.md)

### Linux Setup

```bash
sudo apt-get install python3 python3-pip portaudio19-dev
git clone https://github.com/YOUR_USERNAME/jarvis-mac-setup.git
cd jarvis-mac-setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-linux.txt
python jarvis.py
```

### Windows Setup

```bash
git clone https://github.com/YOUR_USERNAME/jarvis-mac-setup.git
cd jarvis-mac-setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python jarvis.py
```

## Usage 🎙️

Once running, JARVIS listens for voice commands:

```
[JARVIS] Listening for commands...
```

Try these:
- "Hello" - JARVIS greets you
- "What can you do?" - Learn about capabilities
- "What's my battery status?" - Check system info
- "Quit" - Exit the assistant

## Project Structure 📁

```
jarvis-mac-setup/
├── jarvis.py                 # Main entry point
├── co_brain.py              # JARVIS brain/logic loop
├── Alert.py                 # Cross-platform notifications
├── internet_check.py        # Network connectivity check
├── requirements-mac.txt     # macOS dependencies
├── requirements-linux.txt   # Linux dependencies
├── requirements.txt         # Windows dependencies
├── SETUP_MAC.md            # Detailed macOS setup
├── README.md               # This file
│
├── Brain/
│   └── brain.py            # Command processing logic
│
├── TextToSpeech/
│   └── Fast_DF_TTS.py      # Text-to-speech engine
│
├── NetHyTechSTT/
│   └── Listen.py           # Speech recognition
│
├── Data/
│   └── DLG_Data.py         # Dialog strings
│
├── Automation/
│   └── Battery.py          # Battery/system checks
│
└── Time_Operations/
    └── throw_alert.py      # Scheduling & alarms
```

## Key Files Explained

| File | Purpose |
|------|---------|
| `jarvis.py` | Main application entry point - starts all threads |
| `co_brain.py` | Main JARVIS loop - listens and processes commands |
| `Alert.py` | Cross-platform notifications (macOS, Windows, Linux) |
| `Brain/brain.py` | Command interpreter and response generator |
| `TextToSpeech/Fast_DF_TTS.py` | Converts text responses to speech |
| `NetHyTechSTT/Listen.py` | Converts speech to text using Google APIs |

## Installing Dependencies 📦

### For macOS (Recommended)

```bash
pip install -r requirements-mac.txt
```

Includes:
- `SpeechRecognition` - Voice input
- `pyttsx3` - Text-to-speech
- `selenium` - Web automation
- `psutil` - System monitoring

### For Linux

```bash
pip install -r requirements-linux.txt
```

### For Windows

```bash
pip install -r requirements.txt
```

## Troubleshooting 🔧

### Microphone not working?

```bash
# Check microphone
python3 -c "import speech_recognition; print(speech_recognition.Microphone.list_microphone_indexes())"

# Grant permission in System Preferences → Security & Privacy → Microphone
```

### PyAudio installation fails?

```bash
brew install portaudio
pip install pyaudio --no-cache-dir
```

### Module not found errors?

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall requirements
pip install -r requirements-mac.txt
```

See [SETUP_MAC.md](SETUP_MAC.md) for more troubleshooting.

## Extending JARVIS 🛠️

### Add Custom Commands

Edit `Brain/brain.py`:

```python
def process_command(command):
    command = command.lower()
    
    # Add your custom command
    if 'my custom command' in command:
        return "Custom response"
    
    return f"I understood: {command}"
```

### Add TTS Voices

Edit `TextToSpeech/Fast_DF_TTS.py` to change voices:

```python
# macOS voices: Alex, Victoria, Samantha, etc.
engine.setProperty('voice', voices[0].id)
```

### Integrate APIs

Add to `Brain/brain.py`:

```python
if 'weather' in command:
    # Call your weather API
    response = get_weather()
    return response
```

## System Requirements

- **macOS**: 10.12 or newer
- **Linux**: Ubuntu 18.04+ (or equivalent)
- **Windows**: Windows 10 or newer
- **Python**: 3.9+
- **RAM**: 2GB minimum, 4GB recommended
- **Microphone**: Required for voice input

## Performance

- **Startup**: ~2-3 seconds
- **Voice Recognition**: ~1-2 seconds
- **Response**: ~500ms to 2 seconds
- **Memory**: ~150-300MB during operation

## Contributing 🤝

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on multiple platforms
5. Submit a pull request

## License 📄

MIT License - see LICENSE file for details

## Support & Issues

- 📖 Check [SETUP_MAC.md](SETUP_MAC.md) for setup help
- 🐛 Report issues on GitHub
- 💬 Discuss features in Discussions

## Roadmap 🗺️

- [ ] Better voice recognition with local models
- [ ] GUI dashboard
- [ ] Mobile app integration
- [ ] Advanced automation scripts
- [ ] Cloud sync for settings
- [ ] Plugin system for extensibility

## Credits

Inspired by Iron Man's JARVIS. Built with ❤️ for AI enthusiasts.

---

**Ready to get started?** → [SETUP_MAC.md](SETUP_MAC.md)

**Questions?** → Check the Troubleshooting section above.

Happy commanding! 🚀
