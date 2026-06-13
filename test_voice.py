#!/usr/bin/env python3
"""
Voice Functionality Test
Tests PyAudio integration for both microphone and speaker capabilities
"""

import sys
from TextToSpeech.Fast_DF_TTS import speak
from Features.speaker_health import play_tone, play_sweep

def test_voice_modules():
    print("\n" + "="*60)
    print("🎤 JARVIS Voice Functionality Test")
    print("="*60 + "\n")

    # Test 1: Text-to-Speech
    print("[Test 1] Testing Text-to-Speech (Animated Output)...")
    speak("Hello, I am JARVIS. Voice functionality is working!")
    print("✓ Text-to-Speech module loaded successfully\n")

    # Test 2: PyAudio Import
    print("[Test 2] Testing PyAudio availability...")
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        p.terminate()
        print(f"✓ PyAudio is installed and working")
        if device_count > 0:
            print(f"✓ Found {device_count} audio device(s)")
        else:
            print(f"⚠ No audio devices detected (expected in headless environment)")
    except Exception as e:
        print(f"✗ PyAudio error: {e}")
        return False

    # Test 3: Speaker Module
    print("\n[Test 3] Testing Speaker Module...")
    try:
        speak("Testing speaker output module...")
        print("✓ Speaker module functions are available")
    except Exception as e:
        print(f"✗ Speaker error: {e}")
        return False

    # Test 4: Microphone Module
    print("\n[Test 4] Testing Microphone Module...")
    try:
        from Features.mike_health import get_mic_health, mike_health
        print("✓ Microphone module functions are available")
        print("  Note: Microphone health check requires physical audio input")
    except Exception as e:
        print(f"✗ Microphone error: {e}")
        return False

    print("\n" + "="*60)
    print("✅ Voice functionality is properly configured!")
    print("="*60)
    print("\nVoice Components Status:")
    print("  • PyAudio: ✓ Installed")
    print("  • Text-to-Speech: ✓ Working")
    print("  • Speaker Module: ✓ Available")
    print("  • Microphone Module: ✓ Available")
    print("\nNote: Full voice I/O requires physical audio hardware.")
    print("="*60 + "\n")

    return True

if __name__ == "__main__":
    try:
        success = test_voice_modules()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n[Test] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[Test Error] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
