# 🚀 How to Start Maya - Multiple Easy Methods

## Quick Answer: 3 Easy Ways to Launch Maya

### **Method 1: Double-Click Launcher (Easiest) ⭐**
1. Open Finder
2. Navigate to `/Users/[YourUsername]/bp/`
3. **Double-click** `MAYA_FUTURISTIC.command`
4. Maya launches! 🎉

### **Method 2: Terminal Command (Fastest)**
```bash
cd ~/bp && bash MAYA_FUTURISTIC.command
```

### **Method 3: Terminal Alias (Most Convenient)**
```bash
# Add this to ~/.bashrc or ~/.zshrc
alias maya='cd ~/bp && bash MAYA_FUTURISTIC.command'

# Then just type:
maya
```

---

## Detailed Setup for Each Method

### **Method 1: Double-Click to Launch** ⭐ RECOMMENDED

This is the easiest way - just double-click the file!

#### Step 1: Locate the Launcher
```
~/bp/MAYA_FUTURISTIC.command
```

#### Step 2: Double-Click It
- Open Finder
- Go to your `bp` folder
- Double-click `MAYA_FUTURISTIC.command`
- Maya launches automatically!

#### Step 3 (Optional): Add to Dock
1. Open Finder, go to `~/bp/`
2. Right-click `MAYA_FUTURISTIC.command`
3. Select **Options → Add to Dock**
4. Now you can launch Maya from Dock! 

**That's it!** Next time you want to use Maya, just double-click the launcher.

---

### **Method 2: Terminal Command**

Open Terminal and run:
```bash
cd ~/bp && bash MAYA_FUTURISTIC.command
```

This launches Maya immediately.

**To make it even faster:** Create a shell alias (see Method 3)

---

### **Method 3: Create a Terminal Alias** (Best for Frequent Use)

#### Step 1: Open Your Shell Config
```bash
# If you use bash:
nano ~/.bashrc

# If you use zsh (default on new Macs):
nano ~/.zshrc
```

#### Step 2: Add This Alias
```bash
# Add this line at the end of the file
alias maya='cd ~/bp && bash MAYA_FUTURISTIC.command'
```

#### Step 3: Save and Reload
```bash
# Press Ctrl+X, then Y, then Enter to save

# Reload your shell config:
source ~/.bashrc
# or
source ~/.zshrc
```

#### Step 4: Use It!
Now you can launch Maya from anywhere by just typing:
```bash
maya
```

---

### **Method 4: Create a Desktop Shortcut** (macOS)

#### Step 1: Create Shortcut Script
```bash
# Create a simple script on Desktop
cat > ~/Desktop/Start_Maya.sh << 'EOF'
#!/bin/bash
cd ~/bp
bash MAYA_FUTURISTIC.command
EOF

# Make it executable
chmod +x ~/Desktop/Start_Maya.sh
```

#### Step 2: Make It Double-Clickable
1. Right-click the script on Desktop
2. Select **Open With → Other**
3. Choose **Automator.app**
4. Double-click to launch

**Or simpler:** Just double-click `MAYA_FUTURISTIC.command` directly from Finder

---

### **Method 5: Keyboard Shortcut (Advanced)**

Create a keyboard shortcut to launch Maya:

#### On macOS (Using Automator):
1. Open **Automator.app**
2. Create **New → Quick Action**
3. Add **Run Shell Script** action
4. Enter: `cd ~/bp && bash MAYA_FUTURISTIC.command`
5. Save as "Start Maya"
6. Go to **System Settings → Keyboard → Shortcuts**
7. Assign a keyboard shortcut

Now press your shortcut to launch Maya!

---

### **Method 6: Voice Launch** (Fun!)

You can even set up a voice command if you have Siri enabled:

```bash
# Create a script that Siri can trigger
osascript -e 'tell app "Terminal" to do script "cd ~/bp && bash MAYA_FUTURISTIC.command"'
```

Then add to Siri Shortcuts app for voice activation!

---

## Quick Reference Table

| Method | How to Use | Speed | Convenience |
|--------|-----------|-------|-------------|
| **Double-Click** | Click `MAYA_FUTURISTIC.command` | Very Fast | ⭐⭐⭐⭐⭐ |
| **Terminal Command** | Type `cd ~/bp && bash MAYA_FUTURISTIC.command` | Fast | ⭐⭐⭐ |
| **Alias** | Type `maya` | Very Fast | ⭐⭐⭐⭐⭐ |
| **Dock Shortcut** | Click Dock icon | Instant | ⭐⭐⭐⭐⭐ |
| **Desktop Shortcut** | Click Desktop icon | Fast | ⭐⭐⭐⭐ |
| **Keyboard Shortcut** | Press hotkey | Instant | ⭐⭐⭐⭐⭐ |

---

## Step-by-Step: Recommended Setup

### The Easiest Way (Do This Now!)

#### Option A: Dock Icon (My Recommendation)
```bash
# 1. Open Finder
# 2. Go to ~/bp folder
# 3. Find MAYA_FUTURISTIC.command
# 4. Right-click → Options → Add to Dock
# 5. Done! Click Dock icon to launch Maya anytime
```

#### Option B: Terminal Alias
```bash
# 1. Open Terminal
# 2. Run this:
echo "alias maya='cd ~/bp && bash MAYA_FUTURISTIC.command'" >> ~/.zshrc

# 3. Reload:
source ~/.zshrc

# 4. Now type 'maya' to launch anytime!
```

#### Option C: Double-Click Launcher
```bash
# Just double-click ~/bp/MAYA_FUTURISTIC.command
# That's it!
```

---

## Troubleshooting

### "Command not found" error?
Make sure you're in the right directory:
```bash
cd ~/bp
bash MAYA_FUTURISTIC.command
```

### Maya won't open by double-clicking?
1. Right-click the file
2. Select **Open With → Terminal**
3. Or use Terminal command: `cd ~/bp && bash MAYA_FUTURISTIC.command`

### Alias not working?
1. Make sure you edited the right file:
   - For bash: `~/.bashrc`
   - For zsh: `~/.zshrc` (default on new Macs)
2. Reload config: `source ~/.zshrc`
3. Test: `maya` should work

### Can't find MAYA_FUTURISTIC.command?
```bash
# Find it in Terminal
find ~ -name "MAYA_FUTURISTIC.command"

# Then navigate there and run it
bash ~/bp/MAYA_FUTURISTIC.command
```

---

## My Recommended Setup

### For Maximum Convenience:

**1. Add to Dock (Takes 30 seconds)**
```
Finder → ~/bp → MAYA_FUTURISTIC.command
Right-click → Options → Add to Dock
```

**2. Create Terminal Alias (Takes 1 minute)**
```bash
echo "alias maya='cd ~/bp && bash MAYA_FUTURISTIC.command'" >> ~/.zshrc
source ~/.zshrc
```

**Now you have 2 ways to launch Maya:**
- 🖱️ Click Dock icon (instant)
- ⌨️ Type `maya` in Terminal (3 letters!)

---

## One-Command Setup

Run this to set up the alias automatically:
```bash
# For zsh (default on modern Macs)
echo "alias maya='cd ~/bp && bash MAYA_FUTURISTIC.command'" >> ~/.zshrc && source ~/.zshrc && echo "✓ Maya alias created! Type 'maya' to launch"

# For bash (older Macs)
echo "alias maya='cd ~/bp && bash MAYA_FUTURISTIC.command'" >> ~/.bashrc && source ~/.bashrc && echo "✓ Maya alias created! Type 'maya' to launch"
```

---

## Quick Launch Commands

Once set up, use any of these:

```bash
# Method 1: Alias (if you set it up)
maya

# Method 2: Full path
cd ~/bp && bash MAYA_FUTURISTIC.command

# Method 3: Direct Python
python3 ~/bp/jarvis_gui_futuristic.py

# Method 4: From any directory
bash ~/bp/MAYA_FUTURISTIC.command
```

---

## Automating Startup (Optional)

### Start Maya Automatically on Login

```bash
# Create launch agent
mkdir -p ~/Library/LaunchAgents

# Create plist file
cat > ~/Library/LaunchAgents/com.maya.launcher.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.maya.launcher</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>cd ~/bp && bash MAYA_FUTURISTIC.command</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
EOF

# Load the launch agent
launchctl load ~/Library/LaunchAgents/com.maya.launcher.plist
```

Now Maya starts automatically when you log in!

---

## Summary

### **Easiest Options:**

1. **Double-click launcher** → `~/bp/MAYA_FUTURISTIC.command`
2. **Type command** → `cd ~/bp && bash MAYA_FUTURISTIC.command`
3. **Use alias** → `maya` (after setting up)
4. **Click Dock** → Add to Dock first, then click

### **My Recommendation:**
1. Add to Dock (fastest single click)
2. Create alias (fastest typing)
3. You now have two super-fast ways to launch Maya!

---

## Quick Reference

### Next Time You Want to Use Maya:

**Choose one:**
- 🖱️ **Click Dock icon** (if added to Dock)
- ⌨️ **Type `maya`** (if alias set up)
- 📂 **Double-click `MAYA_FUTURISTIC.command`** (always works)
- 🔥 **`cd ~/bp && bash MAYA_FUTURISTIC.command`** (terminal)

That's it! Maya launches instantly! 🚀✨

---

**Pick the method that works best for you and you'll never have to look this up again!**
