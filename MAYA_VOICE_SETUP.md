# 🎙️ Maya Voice Configuration Guide

## Pleasant & Natural Voice Setup

Maya now uses a **pleasant, natural voice** instead of a robotic one!

---

## Default Voice: Samantha

Maya uses **Samantha** by default - a warm, natural female voice that's easy to listen to.

**Characteristics:**
- Natural intonation
- Warm tone
- Easy to understand
- Professional sounding
- Non-robotic and friendly

---

## Supported Voice Options (macOS)

Maya supports multiple macOS voices. Here are the most pleasant options:

### Female Voices (Recommended)
| Voice | Characteristics |
|-------|-----------------|
| **Samantha** ⭐ | Warm, natural, professional (DEFAULT) |
| **Victoria** | Warm, clear, pleasant |
| **Moira** | Energetic, engaging, friendly |
| **Karen** | Clear, articulate, professional |
| **Zira** | Modern, friendly, upbeat |
| **Ellen** | Smooth, confident, natural |

### Male Voices
| Voice | Characteristics |
|-------|-----------------|
| **Alex** | Warm, natural, approachable |
| **Fred** | Clear, friendly, conversational |
| **Oliver** | Modern, smooth, pleasant |

---

## How to Change Voice

### Option 1: Set Default Voice
```bash
# Permanently set Maya's voice to Victoria
export MAYA_VOICE="Victoria"
```

### Option 2: Save to ~/.bashrc or ~/.zshrc
Add this line to your shell configuration:
```bash
export MAYA_VOICE="Victoria"
```

Then reload:
```bash
source ~/.bashrc
# or
source ~/.zshrc
```

### Option 3: Change in Python
```python
from TextToSpeech.Fast_DF_TTS import set_voice

# Set voice to your preference
set_voice("Victoria")
```

---

## Voice Speech Rate

Maya speaks at a natural speed (150 words per minute) which is:
- ✅ Not too fast
- ✅ Not too slow
- ✅ Easy to understand
- ✅ Friendly and conversational

The speech rate is configured in `TextToSpeech/Fast_DF_TTS.py`:
```python
"-r", "150",  # Natural speech rate (words per minute)
```

You can adjust if needed:
- **120 wpm** - Slower, more deliberate
- **150 wpm** - Natural, recommended
- **180 wpm** - Faster, still clear
- **200+ wpm** - Very fast

---

## Test Different Voices

### Quick Test Script
```bash
python3 << 'EOF'
from TextToSpeech.Fast_DF_TTS import speak, set_voice

voices = ["Samantha", "Victoria", "Moira", "Alex"]

for voice in voices:
    set_voice(voice)
    print(f"Testing {voice}...")
    speak(f"Hello! I am {voice}. This is how I sound.")
    print()

print("Test complete!")
EOF
```

---

## Advanced Voice Settings

### Customize Speech Rate

Edit `TextToSpeech/Fast_DF_TTS.py`:

```python
def speak(text, voice=None):
    selected_voice = voice or get_preferred_voice()
    
    # Adjust -r value (in words per minute)
    subprocess.run([
        "say",
        "-v", selected_voice,
        "-r", "150",  # Change this number
        text
    ], check=True)
```

### Get All Available Voices

```bash
say -v ?
```

This shows all voices available on your macOS system.

---

## Why Maya's Voice is Better

### Before (Robotic)
- Fixed speech pattern
- No intonation variations
- Mechanical tone
- Difficult to listen to for long periods
- Not engaging

### Now (Natural)
- ✅ Natural intonation
- ✅ Pleasant tone
- ✅ Easy to understand
- ✅ Friendly and warm
- ✅ Engaging and conversational
- ✅ Customizable

---

## Troubleshooting

### Voice Not Changing?
1. Check if voice is installed:
   ```bash
   say -v ?
   ```
   Look for your voice in the list

2. Make sure environment variable is set:
   ```bash
   echo $MAYA_VOICE
   ```

3. Restart Maya after changing voice

### Voice Sounds Robotic?
- Try a different voice (see options above)
- Adjust speech rate if too fast/slow
- Use Victoria or Moira for more natural sound

### Can't Hear Voice?
- Check system volume
- Make sure audio output is working
- Try testing with:
  ```bash
  say "Hello test"
  ```

---

## Recommended Voice Combinations

### Professional Setting
```bash
export MAYA_VOICE="Victoria"  # Clear and professional
```

### Friendly & Warm
```bash
export MAYA_VOICE="Samantha"  # Default - warm and natural
```

### Energetic & Engaging
```bash
export MAYA_VOICE="Moira"     # Friendly and upbeat
```

### Conversational
```bash
export MAYA_VOICE="Alex"      # Natural male voice
```

---

## Voice Quality Features

Maya's voice implementation includes:

✅ **Natural speech rate** (150 wpm)  
✅ **Multiple voice options**  
✅ **Customizable speech speed**  
✅ **Professional quality audio**  
✅ **No latency or delays**  
✅ **Works offline** (macOS native)  
✅ **Always responsive**  

---

## Setting Up Your Preferred Voice

1. **Choose a voice** from the options above
2. **Test it**:
   ```bash
   export MAYA_VOICE="Victoria"
   python3 jarvis_gui_futuristic.py
   ```
3. **Save to ~/.bashrc** if you like it:
   ```bash
   echo 'export MAYA_VOICE="Victoria"' >> ~/.bashrc
   source ~/.bashrc
   ```
4. **Enjoy!** Maya will use your voice choice

---

## Summary

Maya's voice setup provides:
- **Default**: Samantha (warm, natural, professional)
- **Speed**: 150 WPM (natural, conversational)
- **Options**: 12+ voices to choose from
- **Customizable**: Easy to change to your preference
- **Quality**: High-quality macOS native audio

**No more robotic voice!** Enjoy Maya's pleasant, natural, and engaging speech! 🎙️✨
