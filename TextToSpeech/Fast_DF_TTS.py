import sys
import time

def print_animated_message(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.025)
    print()

def speak(text):
    print_animated_message(text)


#c