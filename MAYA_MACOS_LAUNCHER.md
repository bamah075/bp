# 🌟 Maya macOS Launcher Guide

## Quick Start

Your Maya app is ready to launch! There are two ways to use it:

### Option 1: Double-Click Launcher (Easiest)

1. **From Finder:**
   - Navigate to `/home/user/bp/`
   - Look for **`Maya.app`** folder
   - **Double-click it** to launch Maya
   - Or drag it to your Dock for quick access

2. **From Terminal:**
   ```bash
   /home/user/bp/Maya.app/Contents/MacOS/Maya
   ```

### Option 2: Direct Script

```bash
bash /home/user/bp/launch_maya.sh
```

---

## Setup Instructions

### Add Maya to Your Dock

1. Open Finder
2. Go to: `/home/user/bp/`
3. Find **`Maya.app`**
4. **Drag and drop** it onto your Dock
5. Now you can launch Maya with one click!

### Create a Desktop Shortcut

**Option A: Duplicate to Desktop**
```bash
cp -r /home/user/bp/Maya.app ~/Desktop/Maya.app
```

**Option B: Create Symlink (shows a shortcut icon)**
```bash
ln -s /home/user/bp/Maya.app ~/Desktop/Maya.app
```

---

## Files Created

```
/home/user/bp/
├── Maya.app/                          (The clickable app)
│   └── Contents/
│       ├── Info.plist                 (App configuration)
│       └── MacOS/
│           └── Maya                   (Launcher executable)
├── launch_maya.sh                     (Main launcher script)
└── run_jarvis_gui.sh                  (Legacy launcher)
```

---

## Troubleshooting

### If you see "Error" on Desktop

1. **iCloud storage is full** → Free up space
2. **File permissions issue** → Run:
   ```bash
   chmod +x /home/user/bp/Maya.app/Contents/MacOS/Maya
   chmod +x /home/user/bp/launch_maya.sh
   ```

### If Maya doesn't launch

Try running from Terminal first:
```bash
/home/user/bp/Maya.app/Contents/MacOS/Maya
```

This will show any error messages.

### If dependencies are missing

The launcher will install them automatically, but you can manually install:
```bash
cd /home/user/bp
pip install -r requirements-mac.txt
```

---

## Advanced: Customize the App

### Change the Icon

1. Find a `.icns` file (macOS icon format)
2. Place it at: `/home/user/bp/Maya.app/Contents/Resources/Maya.icns`
3. Edit `/home/user/bp/Maya.app/Contents/Info.plist` and add:
   ```xml
   <key>CFBundleIconFile</key>
   <string>Maya</string>
   ```

### Change the Name

Edit `/home/user/bp/Maya.app/Contents/Info.plist`:
- Change `CFBundleName` to your preferred name
- Change `CFBundleExecutable` if needed

---

## System Requirements

- macOS 10.13 or later
- Python 3.8+
- Virtual environment (venv)
- Dependencies in `requirements-mac.txt`

---

## Launch Maya Now! 🚀

```bash
# Via app
open /home/user/bp/Maya.app

# Via script
bash /home/user/bp/launch_maya.sh

# Via Terminal
/home/user/bp/Maya.app/Contents/MacOS/Maya
```

---

## What Happens When You Launch

1. ✅ Virtual environment is created (if needed)
2. ✅ Dependencies are installed (if needed)
3. ✅ Maya GUI launches with dark mode interface
4. ✅ Voice system loads (Samantha voice)
5. ✅ All super powers APIs ready
6. ✅ Memory system loads previous interactions

**Maya is now running!** 🌟

---

## Next Steps

1. **Add to Dock** - Drag Maya.app to your Dock
2. **Test Commands** - Try: "What can you do?"
3. **Check Memory** - All interactions are saved
4. **Use Super Powers** - Ask about weather or analysis

Enjoy Maya! ✨
