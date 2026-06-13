import sys


def process_command(command):
    """
    Process voice commands and return appropriate responses
    """
    command = command.lower().strip()

    # Greeting commands
    if any(word in command for word in ['hello', 'hi', 'hey']):
        return "Hello! How can I help you?"

    # Exit commands
    if any(word in command for word in ['exit', 'quit', 'bye', 'goodbye']):
        return "Goodbye! Have a great day!"

    # Help command
    if any(word in command for word in ['help', 'what can you do']):
        return "I can help with voice commands, system information, and more. Try asking me anything!"

    # System info
    if 'platform' in command or 'what system' in command:
        platform = sys.platform
        if platform == "darwin":
            return "You're running macOS"
        elif platform == "win32":
            return "You're running Windows"
        else:
            return "You're running Linux"

    # Default response
    return f"I understood: {command}. How would you like me to help?"
