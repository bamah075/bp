# Maya GUI - Professional Voice AI Assistant Interface

## Overview

`jarvis_gui.py` provides a modern, professional graphical interface for Maya with real-time status display, conversation history, and voice control.

## Features

✨ **Professional Design**
- Dark theme with cyan and accent colors
- Real-time microphone level visualization
- Status indicators (Listening, Processing, Speaking, Ready)
- Conversation history with timestamps

🎤 **Voice Control**
- One-click "Listen" button to activate voice input
- Real-time microphone level display
- Animated listening feedback
- Automatic command processing and response

💬 **Conversation Display**
- Scrollable conversation history
- Color-coded user/Maya messages
- Timestamps for each message
- Clear display option

⚙️ **Smart Features**
- Automatic network status detection (Online/Offline)
- Real-time status updates
- Settings window for configuration
- Stop button to cancel listening

## Requirements

- **Python 3.9+**
- **tkinter** (included with Python on Mac, Linux, Windows)
- **PyAudio** (for voice input/output) - ✓ Already installed
- All dependencies from `requirements-mac.txt`

## Installation on Your Mac

### 1. Clone the Repository
```bash
git clone https://github.com/bamah075/bp.git
cd bp
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements-mac.txt
```

### 4. Run Maya GUI
```bash
python3 jarvis_gui.py
```

## Usage

### Starting the Application
1. Run `python3 jarvis_gui.py`
2. The Maya window will open with a professional interface

### Using Voice Commands
1. **Click "🎤 Listen"** - Maya will activate listening mode
2. **Speak your command** - The microphone level bar will show input
3. **Maya processes and responds** - Response appears in conversation
4. **Click "⏹ Stop"** - Stop listening at any time

### Example Commands
- "Hello" - Get a greeting
- "What can you do" - Learn about Maya capabilities
- "What system am I on" - Check system information
- "Help" - Get help information

### Controls
- **🎤 Listen** - Activate voice listening mode
- **⏹ Stop** - Stop listening
- **🗑 Clear** - Clear conversation history
- **⚙ Settings** - Access settings panel

### Status Indicators
- **●** (Green) - Online and connected
- **●** (Orange) - Offline or checking connection
- **🎤 Ready to listen** - Waiting for voice input
- **🎤 Listening...** - Actively listening for commands
- **🧠 Processing...** - Processing your command
- **🔊 Speaking...** - Maya is responding

## GUI Components Explained

### Header Section
- Maya logo and title
- Network status indicator (Online/Offline)
- Connection status display

### Status Section
- Current listening/processing status with emoji
- Microphone level visualization
- Real-time audio input feedback

### Conversation Display
- Full conversation history
- Color-coded messages:
  - **Cyan**: Your voice commands
  - **Green**: Maya responses
  - **Gray**: Timestamps

### Control Buttons
- **Listen**: Activate voice mode
- **Stop**: Stop listening
- **Clear**: Reset conversation
- **Settings**: Configuration options

### Footer
- Version information
- Quick status text

## Customization

### Change Colors
Edit the color constants in `JARVISGui.create_styles()`:
```python
self.primary_color = "#00d9ff"    # Cyan
self.accent_color = "#ff006e"     # Pink
self.success_color = "#06ffa5"    # Green
self.warning_color = "#ffa500"    # Orange
```

### Adjust Window Size
Modify the geometry in `__init__()`:
```python
self.root.geometry("900x700")  # Change to your preferred size
```

### Configure Voice Settings
Edit voice parameters in the Voice Modules:
- `Features/mike_health.py` - Microphone settings
- `Features/speaker_health.py` - Speaker settings
- `TextToSpeech/Fast_DF_TTS.py` - Text-to-Speech settings

## Troubleshooting

### "No module named tkinter"
**On Mac**: Tkinter is included with Python. Make sure you're using system Python or Homebrew Python
```bash
# Check if tkinter is available
python3 -m tkinter
```

### "PyAudio not found"
```bash
source venv/bin/activate
pip install pyaudio
```

### "No microphone detected"
- Check System Preferences > Security & Privacy > Microphone
- Ensure the app has microphone permissions
- Test microphone with: `python3 test_voice.py`

### GUI doesn't respond
- Make sure you're running in the virtual environment
- Check that all dependencies are installed
- Restart the application

## Next Steps

1. **Clone to your Mac** and run `python3 jarvis_gui.py`
2. **Test voice input** - Use "Listen" button to speak
3. **Add custom commands** in `Brain/brain.py` to extend Maya
4. **Customize the interface** to match your preferences
5. **Set up keyboard shortcuts** (optional enhancement)

## Voice Integration Details

The GUI integrates with:
- **PyAudio**: Real-time audio input/output (installed ✓)
- **Voice Recognition**: Processes spoken commands
- **Brain Module**: `Brain/brain.py` handles command processing
- **Text-to-Speech**: `TextToSpeech/Fast_DF_TTS.py` provides responses
- **Features**: `Features/mike_health.py` and `speaker_health.py` for audio health

## Architecture

```
jarvis_gui.py (Main GUI Application)
├── tkinter (Display Layer)
├── Brain/brain.py (Command Processing)
├── TextToSpeech/Fast_DF_TTS.py (Voice Output)
├── Features/mike_health.py (Voice Input)
└── Features/speaker_health.py (Audio Playback)
```

## Performance Notes

- Initial load time: ~2-3 seconds
- Voice response time: ~1-2 seconds (depends on command complexity)
- CPU usage: Minimal (~5-10% during operation)
- Memory usage: ~50-100 MB

## Support

For issues or questions:
1. Check `test_voice.py` to verify voice components
2. Review `demo.py` for command processing verification
3. Check voice module imports with `python3 -c "from Features.mike_health import *"`

## Version History

**v1.0** (Current)
- Professional dark-themed GUI
- Voice activation and command processing
- Real-time status display
- Conversation history with timestamps
- Settings panel
- Network status detection

---

**Ready to use! Just run on your Mac and start speaking.** 🎤
