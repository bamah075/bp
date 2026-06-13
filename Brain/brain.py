import sys
if sys.version_info < (3, 10):
    try:
        from typing_extensions import TypeAlias
        sys.modules['typing'].TypeAlias = TypeAlias
    except ImportError:
        pass

try:
    from webscout import Perplexity
except ImportError:
    from webscout import OpenRouter

def Main_Brain(text):
    try:
        ai = Perplexity(timeout=30, quiet=True)
        res = ai.chat(text)
        return res
    except Exception:
        return f"I understood: {text}. Unable to process at the moment."

def process_command(text):
    return Main_Brain(text)

