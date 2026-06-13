def Main_Brain(text):
    responses = {
        "hello": "Hello! How can I help you?",
        "hi": "Hi there! What do you need?",
        "what can you do": "I can help with system information, weather, image recognition, and various automation tasks.",
        "what system am i on": "You're running JARVIS on macOS or Linux.",
        "help": "I'm JARVIS, your AI assistant. Ask me about system info, weather, or just chat!",
    }

    text_lower = text.lower().strip()
    for key, response in responses.items():
        if key in text_lower:
            return response

    return f"I understand: {text}. How can I help?"

def process_command(text):
    return Main_Brain(text)

