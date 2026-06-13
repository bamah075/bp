# J.A.R.V.I.S Setup Guide for Linux 🐧

This guide helps you set up J.A.R.V.I.S on Linux with full cross-platform compatibility.

## Prerequisites

- Linux distribution (Ubuntu, Debian, Fedora, etc.)
- Python 3.7 or newer
- Microphone for voice input
- 2GB+ RAM recommended

## Installation Steps

### 1. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv
sudo apt-get install -y portaudio19-dev alsa-utils
sudo apt-get install -y libffi-dev libssl-dev
```

**Fedora/RHEL:**
```bash
sudo dnf install python3 python3-pip python3-devel
sudo dnf install portaudio-devel alsa-utils
```

**Arch:**
```bash
sudo pacman -S python pip portaudio
```

### 2. Clone the Repository

```bash
git clone https://github.com/AnubhavChaturvedi-GitHub/jarvis-ai-assistant.git
cd jarvis-ai-assistant
```

### 3. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements-core.txt
```

If you want additional features (requires more dependencies):
```bash
pip install -r requirements-linux.txt
```

### 5. Run J.A.R.V.I.S

```bash
python jarvis.py
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'winotify'"
**Solution**: This is expected on Linux. The cross-platform Alert system automatically uses console output instead.

### Issue: PyAudio installation fails
```bash
# Install additional audio development files
sudo apt-get install -y libportaudio2 libportaudiocpp0

# Try installing PyAudio again
pip install pyaudio --no-cache-dir
```

### Issue: Microphone not recognized
```bash
# Check audio devices
arecord -l

# Test microphone
arecord -d 5 test_audio.wav

# Verify PulseAudio is running
pulseaudio --version
```

### Issue: Import errors for GUI libraries
**Solution**: Some GUI automation features (pygetwindow, pyautogui) don't fully work on Linux.  
These features are optional - the core AI functionality works fine without them.

```bash
# Skip problematic packages
pip install --no-deps pywhatkit
```

### Issue: Permission denied for audio/microphone
```bash
# Add user to audio group
sudo usermod -a -G audio $USER
# Log out and log back in
```

---

## Features Working on Linux

✅ Voice command listening  
✅ AI conversation  
✅ Text-to-speech responses  
✅ System notifications  
✅ Web automation (Selenium)  
✅ Weather checking  
✅ Image generation  
✅ Vision/camera features  
❌ System brightness control  
⚠️ Audio volume control (partial)  
❌ WhatsApp automation  

---

## Useful Linux Commands

```bash
# Check audio devices
aplay -l
pactl list short sources

# Test microphone
ffmpeg -f pulse -i default -t 5 test_audio.wav

# Monitor system audio
watch -n 1 pactl list sinks

# Check system resources
free -h
ps aux | grep jarvis
```

---

## Known Limitations on Linux

1. **System Control**: Brightness, volume limited by desktop environment
2. **Notifications**: Limited to console output
3. **GUI Automation**: pyautogui features restricted
4. **WhatsApp**: Web-based automation not fully supported
5. **Desktop Integration**: Varies by distribution and desktop environment

---

## Using with Systemd

Create a service to auto-start J.A.R.V.I.S:

```bash
sudo nano /etc/systemd/user/jarvis.service
```

Add this content:
```ini
[Unit]
Description=J.A.R.V.I.S AI Assistant
After=network.target

[Service]
Type=simple
User=%i
WorkingDirectory=/home/%i/jarvis-ai-assistant
ExecStart=/home/%i/jarvis-ai-assistant/venv/bin/python jarvis.py
Restart=always

[Install]
WantedBy=default.target
```

Enable and start:
```bash
systemctl --user enable jarvis
systemctl --user start jarvis
systemctl --user status jarvis
```

---

## Docker Setup (Alternative)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y portaudio19-dev
COPY requirements-core.txt .
RUN pip install -r requirements-core.txt
COPY . .
CMD ["python", "jarvis.py"]
```

Build and run:
```bash
docker build -t jarvis .
docker run -it --device /dev/snd jarvis
```

---

## Performance Optimization

For resource-constrained systems:

1. **Disable threading**: Edit `jarvis.py` to reduce concurrent threads
2. **Use core requirements**: Use `requirements-core.txt` only
3. **Disable vision**: Comment out vision imports
4. **Limit history**: Clear log files periodically

```bash
# Monitor resource usage
top -p $(pgrep -f jarvis.py)
```

---

## Environment Variables

```bash
# Enable debug mode
export JARVIS_DEBUG=1

# Specify audio device
export AUDIO_DEVICE=default

# Set logging level
export LOGLEVEL=INFO
```

---

## Support

For Linux-specific issues:
1. Check `/var/log/syslog` for system errors
2. Run with debug: `JARVIS_DEBUG=1 python jarvis.py`
3. Test audio: `arecord -d 2 | aplay`

---

## Next Steps

1. Configure speech synthesis settings
2. Create custom voice commands
3. Set up external integrations
4. Optimize for your specific Linux distribution

Enjoy your Linux J.A.R.V.I.S experience! 🚀
