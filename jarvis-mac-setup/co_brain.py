import sys
from NetHyTechSTT.Listen import Listener
from TextToSpeech.Fast_DF_TTS import speak
from Brain.brain import process_command


def Jarvis():
    """
    Main JARVIS brain loop - listens to voice commands and processes them
    """
    print("[JARVIS] Listening for commands...")
    listener = Listener()

    while True:
        try:
            # Listen for voice input
            command = listener.listen()

            if command:
                print(f"[JARVIS] You said: {command}")

                # Process the command
                response = process_command(command)

                if response:
                    print(f"[JARVIS] {response}")
                    speak(response)

        except KeyboardInterrupt:
            print("\n[JARVIS] Shutting down...")
            break
        except Exception as e:
            print(f"[JARVIS Error] {e}")
            continue
