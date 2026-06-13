# J.A.R.V.I.S Platform Compatibility Guide

This document explains the cross-platform modifications made to run J.A.R.V.I.S on Windows, macOS, and Linux.

## Overview

The original J.A.R.V.I.S was designed for Windows. The following changes enable it to run on macOS and Linux with graceful fallbacks.

## Modified Modules

### 1. Alert System (`Alert.py`)

**Original (Windows-only):**
- Used `winotify` for toast notifications
- Displayed Windows-style notification popups

**Updated (Cross-platform):**
```python
- Windows: Uses winotify for native toast notifications
- macOS: Uses osascript for native system notifications
- Linux: Falls back to console output
```

**File**: `/home/user/bp/Alert.py`

### 2. Brightness Control (`Features/set_br.py`)

**Original (Windows-only):**
- Used WMI (Windows Management Instrumentation)
- Required Windows-specific system APIs

**Updated (Cross-platform):**
```python
- Windows: Uses WMI for direct brightness control
- macOS: Uses osascript to adjust brightness
- Linux: Gracefully skips or uses limited gnome-brightness
```

**File**: `/home/user/bp/Features/set_br.py`

### 3. Brightness Reading (`Features/br_persentage.py`)

**Original (Windows-only):**
- Used WMI to query current brightness

**Updated (Cross-platform):**
```python
- Windows: Uses WMI queries
- macOS: Uses ioreg command with fallback
- Linux: Returns unavailable status
```

**File**: `/home/user/bp/Features/br_persentage.py`

### 4. File Paths (`jarvis.py`)

**Original (Windows):**
```python
path = f"{getcwd()}\\Alam_data.txt"  # Windows backslash
```

**Updated (Cross-platform):**
```python
path = os.path.join(getcwd(), "Alam_data.txt")  # Platform-agnostic
```

**File**: `/home/user/bp/jarvis.py`

---

## Platform-Specific Features

### Windows ✅
- **Full Compatibility**: All features work as intended
- **Notifications**: Native toast notifications
- **System Control**: Full brightness, volume, audio control
- **Automation**: All GUI automation features

### macOS ⚠️
- **Partially Supported**: Core features work
- **Notifications**: Native Notification Center
- **System Control**: Limited brightness control via osascript
- **Limitations**: Some GUI automation features restricted by security
- **Recommended**: Use `requirements-mac.txt`

### Linux ⚠️
- **Limited Support**: Core AI features work
- **Notifications**: Console output only
- **System Control**: Very limited (desktop environment dependent)
- **Limitations**: Most system-level features unavailable
- **Recommended**: Use `requirements-core.txt` for stability

---

## Requirements Files

### `requirements.txt` (Windows)
Full functionality with all Windows-specific packages

### `requirements-mac.txt`
macOS-optimized:
- Excludes `winotify`, `wmi`, `pycaw`, `comtypes`
- Includes `pyttsx3` for alternative TTS
- Platform-aware implementations

### `requirements-core.txt`
Minimal dependencies:
- Only essential packages
- Most reliable across platforms
- Reduced features but maximum stability

### `requirements-linux.txt`
Linux-compatible:
- Excludes Windows-only packages
- Attempts more features than `-core`
- May have build issues on some systems

---

## Compatibility Matrix

| Feature | Windows | macOS | Linux |
|---------|---------|-------|-------|
| Voice Recognition | ✅ | ✅ | ✅ |
| Text-to-Speech | ✅ | ✅ | ✅ |
| AI Conversation | ✅ | ✅ | ✅ |
| Notifications | ✅ | ✅ | ⚠️ |
| Brightness Control | ✅ | ⚠️ | ❌ |
| Volume Control | ✅ | ⚠️ | ⚠️ |
| System Monitoring | ✅ | ✅ | ✅ |
| Web Automation | ✅ | ✅ | ✅ |
| Camera/Vision | ✅ | ✅ | ✅ |
| Weather API | ✅ | ✅ | ✅ |
| WhatsApp (Web) | ✅ | ⚠️ | ⚠️ |

---

## Implementation Details

### Alert System Logic

```python
def Alert(Text):
    if sys.platform == "win32":
        # Windows implementation
        from winotify import Notification
        # Show toast notification
    elif sys.platform == "darwin":
        # macOS implementation
        subprocess.run(["osascript", "-e", script])
        # Show Notification Center notification
    else:
        # Linux/other implementation
        print(f"Alert: {Text}")
```

### Brightness Control Logic

```python
def set_brightness_windows(percentage):
    if sys.platform == "win32":
        # Windows WMI method
    elif sys.platform == "darwin":
        # macOS osascript method
    else:
        # Fallback or unavailable
```

### Path Handling

All file operations now use:
```python
os.path.join(getcwd(), "filename.txt")
```

Instead of:
```python
f"{getcwd()}\\filename.txt"  # Windows only
```

---

## Testing on Different Platforms

### Quick Test on Windows
```bash
python jarvis.py
# All features should work
```

### Quick Test on macOS
```bash
python -c "import sys; print('Platform:', sys.platform)"
# Should print: darwin
python jarvis.py
# Core features + notifications work
```

### Quick Test on Linux
```bash
python -c "import sys; print('Platform:', sys.platform)"
# Should print: linux
python jarvis.py
# Core features work, system control limited
```

---

## Fallback Strategy

The code uses try-except blocks with platform detection:

```python
try:
    if platform == "win32":
        # Windows-specific code
        windows_function()
    elif platform == "darwin":
        # macOS-specific code
        macos_function()
    else:
        # Linux/generic code
        generic_function()
except ImportError:
    # Graceful fallback if module not available
    print("Feature unavailable on this platform")
except Exception as e:
    # Catch and report errors
    print(f"Error: {e}")
```

---

## Adding Cross-Platform Support to New Features

When adding new features:

1. **Check Platform**: `import sys; sys.platform`
2. **Implement Variants**: Create platform-specific implementations
3. **Use Fallbacks**: Provide graceful degradation
4. **Update Requirements**: Add new packages to appropriate requirements file
5. **Test All Platforms**: Verify on Windows, macOS, and Linux

Example:
```python
import sys

def new_feature():
    try:
        if sys.platform == "win32":
            return windows_implementation()
        elif sys.platform == "darwin":
            return macos_implementation()
        else:
            return linux_implementation()
    except Exception as e:
        print(f"Feature unavailable: {e}")
        return None
```

---

## Contributing

When contributing:
- Test on at least 2 different platforms
- Include platform checks for OS-specific code
- Update compatibility documentation
- Test with minimal requirements first
- Document any new limitations

---

## Future Improvements

Planned cross-platform enhancements:
- [ ] Better macOS brightness API
- [ ] Linux desktop environment detection
- [ ] Universal notification system
- [ ] Multi-platform testing CI/CD
- [ ] Container-based deployment

---

## References

- [Python sys.platform](https://docs.python.org/3/library/sys.html#sys.platform)
- [Python os.path](https://docs.python.org/3/library/os.path.html)
- [macOS scripting with osascript](https://ss64.com/osx/osascript.html)
- [Linux ALSA Audio](https://alsa-project.org/)
