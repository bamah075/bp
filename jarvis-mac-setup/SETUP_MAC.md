# J.A.R.V.I.S Setup Guide for macOS 🍎

Quick and easy setup for JARVIS AI Assistant on your Mac.

## Prerequisites

- macOS 10.12 or newer
- Homebrew installed
- Python 3.9 or newer
- Microphone for voice input

## Quick Start (Copy & Paste)

```bash
# 1. Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install Python and audio libraries
brew install python@3.11 portaudio

# 3. Clone JARVIS
git clone https://github.com/YOUR_USERNAME/jarvis-mac-setup.git
cd jarvis-mac-setup

# 4. Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# 5. Install Python packages
pip install --upgrade pip
pip install -r requirements-mac.txt

# 6. Run JARVIS
python jarvis.py
```

## Detailed Setup Steps

### Step 1: Install Homebrew

If you don't have Homebrew installed:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Add Homebrew to PATH (if needed):
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### Step 2: Install System Dependencies

```bash
# Install Python 3.11 (recommended)
brew install python@3.11 portaudio

# Verify installation
python3.11 --version
brew list portaudio
```

### Step 3: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/jarvis-mac-setup.git
cd jarvis-mac-setup
```

### Step 4: Create Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
```

Your terminal should now show `(venv)` prefix.

### Step 5: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements-mac.txt
```

This installs:
- Speech Recognition (voice input)
- Text-to-Speech (voice output)
- Selenium (web automation)
- And other essential packages

### Step 6: Grant Microphone Permissions

When you run JARVIS for the first time, macOS will prompt you to allow microphone access. Click "Allow".

### Step 7: Run JARVIS

```bash
python jarvis.py
```

You should see:
```
[JARVIS] Listening for commands...
```

Try saying: "Hello" or "What can you do?"

---

## Troubleshooting

### Issue: "No module named 'speech_recognition'"

```bash
pip install SpeechRecognition
```

### Issue: PyAudio installation fails

```bash
# Use Homebrew to install PortAudio first
brew install portaudio

# Then install PyAudio
pip install pyaudio
```

If that still fails, try:
```bash
LDFLAGS=-L/usr/local/opt/portaudio/lib CPPFLAGS=-I/usr/local/opt/portaudio/include pip install pyaudio
```

### Issue: Microphone not recognized

```bash
# Check audio devices
python3 -c "import pyaudio; p = pyaudio.PyAudio(); print([p.get_device_info_by_index(i) for i in range(p.get_device_count())])"

# Test microphone
ffmpeg -f avfoundation -i ":0" -t 5 test_audio.wav
aplay test_audio.wav
```

### Issue: "ModuleNotFoundError" for other packages

Simply reinstall requirements:
```bash
source venv/bin/activate
pip install -r requirements-mac.txt
```

### Issue: JARVIS won't listen to voice commands

1. Check microphone permissions in System Preferences → Security & Privacy → Microphone
2. Ensure Terminal/VS Code has microphone access
3. Test with: `python3 -c "import speech_recognition as sr; sr.Microphone().list_microphone_indexes()"`

---

## Creating an Alias for Easy Launch

Add this to your `~/.zprofile` or `~/.bash_profile`:

```bash
alias jarvis="source ~/jarvis-mac-setup/venv/bin/activate && python ~/jarvis-mac-setup/jarvis.py"
```

Then reload:
```bash
source ~/.zprofile
```

Now you can just type `jarvis` to start!

---

## Features

✅ Voice command listening  
✅ AI responses with text-to-speech  
✅ Command processing  
✅ Battery/system information  
✅ Cross-platform compatible  

---

## Performance Tips

1. **Close unnecessary apps** to free up resources
2. **Use M1/M2 Macs** for best performance
3. **Reduce background tasks** if experiencing lag
4. **Monitor with Activity Monitor**: `cmd + space` → "Activity Monitor"

---

## Environment Variables (Optional)

```bash
# Enable debug logging
export JARVIS_DEBUG=1

# Set specific voice
export JARVIS_VOICE=Victoria  # Options: Alex, Victoria, Samantha, etc.

# Set audio device (if you have multiple microphones)
export AUDIO_DEVICE_ID=<id>
```

---

## Next Steps

1. Customize voice commands in `Brain/brain.py`
2. Add integrations with APIs
3. Create macOS-specific automations with AppleScript
4. Explore advanced features in subdirectories

---

## Support

- Check the **Troubleshooting** section above
- Run with debug: `JARVIS_DEBUG=1 python jarvis.py`
- Check system logs: `log stream --predicate 'eventMessage contains "jarvis"'`

---

## Known Limitations on macOS

1. Some GUI automation features require accessibility permissions
2. System brightness control limited by macOS security
3. WhatsApp automation not fully supported (use web version)

---

Enjoy your JARVIS assistant! 🚀
