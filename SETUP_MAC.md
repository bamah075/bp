# J.A.R.V.I.S Setup Guide for macOS 🍎

This guide helps you set up J.A.R.V.I.S on your Mac with full cross-platform compatibility.

## Prerequisites

- macOS 10.12 or newer
- Homebrew installed
- Python 3.7 or newer
- Microphone for voice input

## Installation Steps

### 1. Install Homebrew (if not already installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install System Dependencies

```bash
# Install Python 3.11 and audio libraries
brew install python@3.11 portaudio

# Verify installation
python3 --version
```

### 3. Clone the Repository

```bash
git clone https://github.com/AnubhavChaturvedi-GitHub/jarvis-ai-assistant.git
cd jarvis-ai-assistant
```

### 4. Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements-mac.txt
```

### 6. Grant Permissions

J.A.R.V.I.S needs several permissions on macOS. When you run it for the first time:

1. **Microphone Access**: System will prompt you. Click "Allow"
2. **Automation**: Grant Terminal access in System Preferences → Security & Privacy → Automation

### 7. Run J.A.R.V.I.S

```bash
python jarvis.py
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'winotify'"
**Solution**: This is expected on macOS. The cross-platform Alert system automatically uses macOS notifications instead.

### Issue: PyAudio installation fails
```bash
pip install pyaudio --no-cache-dir
# If still fails, try:
LDFLAGS=-L/usr/local/opt/portaudio/lib CPPFLAGS=-I/usr/local/opt/portaudio/include pip install pyaudio
```

### Issue: "playsound" module not working
```bash
pip install --upgrade playsound
# Or use alternative:
pip install pyttsx3  # Text-to-speech fallback
```

### Issue: Microphone not detected
```bash
# Check audio devices
python -c "import pyaudio; p = pyaudio.PyAudio(); print([p.get_device_info_by_index(i) for i in range(p.get_device_count())])"
```

### Issue: Notifications not appearing
The cross-platform Alert system supports:
- **Windows**: Windowed toast notifications
- **macOS**: Native system notifications via osascript
- **Linux**: Console output

On macOS, notifications appear in the Notification Center (top-right corner).

---

## Features Working on macOS

✅ Voice command listening  
✅ AI conversation  
✅ Text-to-speech responses  
✅ System notifications  
✅ Web automation (Selenium)  
✅ Weather checking  
✅ Image generation  
✅ Vision/camera features  
⚠️ System brightness (limited)  
⚠️ Audio volume control (partial)  

---

## Useful macOS Commands

```bash
# Check microphone levels
audio_coreaudio_utility check-device

# List audio devices
system_profiler SPAudioDataType

# Test microphone
ffmpeg -f avfoundation -i ":0" -t 5 test_audio.wav

# Grant microphone permission (if needed)
defaults write com.apple.AppleSDWebKit NSAllowsLocalFileAccess -bool true
```

---

## Known Limitations on macOS

1. **Brightness Control**: Limited by macOS security restrictions
2. **System Audio**: Some advanced audio controls unavailable
3. **Process Automation**: WhatsApp automation requires manual setup
4. **Screen Control**: Limited clipboard and automation features

---

## Environment Variables

```bash
# Enable debug logging
export JARVIS_DEBUG=1

# Specify audio device (get device ID from audio check)
export AUDIO_DEVICE_ID=<id>

# Set voice (Matthew, Samantha, Victoria, etc.)
export JARVIS_VOICE=Samantha
```

---

## Virtual Environment

To always activate the environment:

```bash
# Create alias in ~/.zshrc or ~/.bash_profile
echo 'alias jarvis="source ~/path/to/jarvis-ai-assistant/venv/bin/activate && python jarvis.py"' >> ~/.zshrc
source ~/.zshrc

# Then simply run:
jarvis
```

---

## Performance Tips

1. **Reduce Threading**: Disable non-essential threads in `jarvis.py` for slower Macs
2. **Disable Vision**: Comment out vision-related imports if you don't need it
3. **Use Core Requirements**: Try `requirements-core.txt` for minimal overhead

---

## Support

For issues specific to macOS:
1. Check the troubleshooting section above
2. Review system audio settings
3. Verify all permissions are granted
4. Check system logs: `log stream --predicate 'eventMessage contains "jarvis"'`

---

## Next Steps

1. Configure speech voices in `co_brain.py`
2. Set up WhatsApp automation (manual)
3. Create custom commands in `Brain/brain.py`
4. Adjust notification settings as needed

Enjoy your macOS J.A.R.V.I.S experience! 🎉
