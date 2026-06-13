# J.A.R.V.I.S Platform Compatibility Guide

Cross-platform support for Windows, macOS, and Linux.

## Supported Platforms

| Platform | Status | Recommended | Features |
|----------|--------|-------------|----------|
| macOS | ✅ Fully Supported | Yes | All features |
| Linux | ✅ Supported | - | Core features |
| Windows | ✅ Fully Supported | - | All features |

## Platform Detection

The application uses Python's `sys.platform` for detection:

```python
import sys

if sys.platform == "darwin":
    # macOS code
elif sys.platform == "win32":
    # Windows code
else:
    # Linux/other code
```

## Feature Compatibility Matrix

| Feature | macOS | Windows | Linux |
|---------|-------|---------|-------|
| Voice Input | ✅ | ✅ | ✅ |
| Text Output | ✅ | ✅ | ✅ |
| Notifications | ✅ | ✅ | ⚠️ |
| Brightness Control | ⚠️ | ✅ | ❌ |
| Battery Check | ✅ | ✅ | ✅ |
| Web Automation | ✅ | ✅ | ✅ |

Legend: ✅ = Full Support, ⚠️ = Limited, ❌ = Not Available

## Cross-Platform Implementations

### 1. Alert System (Alert.py)

**macOS**: Uses `osascript` for native Notification Center notifications

```python
if sys.platform == "darwin":
    script = 'display notification "message" with title "JARVIS"'
    subprocess.run(["osascript", "-e", script])
```

**Windows**: Uses `winotify` for toast notifications

```python
if sys.platform == "win32":
    from winotify import Notification
    notification.show()
```

**Linux**: Console output fallback

```python
else:
    print(f"[Alert] {message}")
```

### 2. Text-to-Speech (TextToSpeech/Fast_DF_TTS.py)

Uses `pyttsx3` which works across all platforms:

```python
import pyttsx3
engine = pyttsx3.init()

if sys.platform == "darwin":
    engine.setProperty('rate', 150)  # macOS settings
elif sys.platform == "win32":
    engine.setProperty('rate', 150)  # Windows settings
else:
    engine.setProperty('rate', 150)  # Linux settings

engine.say("Your message")
engine.runAndWait()
```

### 3. Speech Recognition (NetHyTechSTT/Listen.py)

Uses `SpeechRecognition` library with Google Speech API:

```python
import speech_recognition as sr

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    audio = recognizer.listen(source)
    text = recognizer.recognize_google(audio)
```

Works identically on all platforms.

### 4. File Paths (jarvis.py)

Uses `os.path.join()` for cross-platform paths:

```python
# ✅ Correct - Cross-platform
path = os.path.join(getcwd(), "Alam_data.txt")

# ❌ Wrong - Windows only
path = f"{getcwd()}\\Alam_data.txt"
```

### 5. Brightness Control (Features/set_br.py)

**macOS**: AppleScript

```python
script = 'tell application "System Events" to set brightness to 0.75'
subprocess.run(["osascript", "-e", script])
```

**Windows**: WMI

```python
import wmi
methods = wmi.WMI().WmiMonitorBrightnessMethods()
methods[0].WmiSetBrightness(Brightness=75)
```

**Linux**: Not fully supported (desktop environment dependent)

### 6. Battery Status (Automation/Battery.py)

**macOS**: `pmset` command

```python
result = subprocess.run(["pmset", "-g", "batt"], capture_output=True)
```

**Windows**: WMI query

```python
result = subprocess.run(["wmic", "path", "win32_battery", "get", ...])
```

**Linux**: `acpi` command

```python
result = subprocess.run(["acpi", "-b"], capture_output=True)
```

## Requirements Files

### requirements-mac.txt
Optimized for macOS:
- Core dependencies
- macOS-specific packages
- No Windows-only libraries

### requirements.txt (Windows)
Full-featured Windows setup:
- All dependencies
- Windows-specific packages (winotify, wmi, pycaw)
- GUI automation tools

### requirements-linux.txt
Linux-compatible dependencies:
- Core packages
- Linux-compatible alternatives
- No Windows-specific libraries

## Virtual Environment Setup

### macOS & Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-mac.txt  # or requirements-linux.txt
```

### Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Error Handling Strategy

All platform-specific code uses try-except blocks:

```python
try:
    if sys.platform == "darwin":
        # macOS implementation
    elif sys.platform == "win32":
        # Windows implementation
    else:
        # Linux/fallback implementation
except ImportError:
    print("Feature not available on this platform")
except Exception as e:
    print(f"Error: {e}")
```

## Testing on Different Platforms

### Quick platform check:
```bash
python -c "import sys; print(f'Platform: {sys.platform}')"
```

### Expected outputs:
- macOS: `darwin`
- Windows: `win32`
- Linux: `linux`

## Performance Comparison

| Operation | macOS | Windows | Linux |
|-----------|-------|---------|-------|
| Startup | ~2-3s | ~2-3s | ~2-3s |
| Voice Recognition | ~1-2s | ~1-2s | ~1-2s |
| Text-to-Speech | ~0.5-1s | ~0.5-1s | ~0.5-1s |
| Battery Check | <100ms | <100ms | <100ms |

## Limitations

### macOS
- Brightness control limited by system permissions
- Some automation features require accessibility settings
- WhatsApp automation not fully supported

### Linux
- Brightness control very limited (desktop environment dependent)
- Notifications only via console
- GUI automation features restricted

### Windows
- Requires administrator access for some features
- Some WMI calls may fail on Home editions

## Adding Cross-Platform Support

When adding new features:

1. **Use platform detection**:
   ```python
   import sys
   if sys.platform == "darwin":
       # macOS specific
   ```

2. **Provide fallbacks**:
   ```python
   try:
       # Try preferred method
   except:
       # Fallback
   ```

3. **Test on all platforms** before committing

4. **Update requirements files** with new dependencies

5. **Document limitations** in this file

## Resources

- [Python sys.platform](https://docs.python.org/3/library/sys.html)
- [os.path documentation](https://docs.python.org/3/library/os.path.html)
- [Subprocess module](https://docs.python.org/3/library/subprocess.html)
- [macOS scripting with osascript](https://ss64.com/osx/osascript.html)

## Support

For platform-specific issues:

1. Check the Troubleshooting section in SETUP_MAC.md
2. Run with debug: `python -c "import sys; print(sys.platform)"`
3. Check error logs for detailed information
