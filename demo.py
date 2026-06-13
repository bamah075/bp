#!/usr/bin/env python3
"""
JARVIS Demo - Test without voice input
Run this to verify JARVIS is working correctly
"""

import sys
from TextToSpeech.Fast_DF_TTS import speak
from Brain.brain import process_command
from internet_check import is_Online
from Data.DLG_Data import online_dlg, offline_dlg
import random


def demo():
    print("\n" + "="*50)
    print("🤖 J.A.R.V.I.S Demo Mode")
    print("="*50 + "\n")

    # Check network
    try:
        online = is_Online()
    except Exception:
        online = False

    status = random.choice(online_dlg if online else offline_dlg)
    print(f"[JARVIS] {status}\n")

    # Test commands
    test_commands = [
        "hello",
        "what can you do",
        "what system am i on",
        "quit"
    ]

    print("[Demo] Testing voice command processing:\n")

    for cmd in test_commands:
        print(f"📢 User: {cmd}")
        response = process_command(cmd)
        print(f"🤖 JARVIS: {response}\n")

    print("="*50)
    print("✅ Demo complete! JARVIS is working correctly.")
    print("="*50 + "\n")
    print("To run JARVIS with voice input, use:")
    print("  python jarvis.py\n")


if __name__ == "__main__":
    try:
        demo()
    except KeyboardInterrupt:
        print("\n\n[JARVIS] Demo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[JARVIS Error] {e}")
        sys.exit(1)
