"""
EXECUTE layer — single-purpose tool: save_file
Unix philosophy: does one thing, deterministically, with typed I/O.
"""
import sys
from pathlib import Path


def save_file(content: str, path: str, encoding: str = "utf-8") -> dict:
    """
    Write content to path. Creates parent dirs automatically.
    Returns a typed result dict — never raises on write failure (degrades gracefully).

    Non-negotiable #4: degrades gracefully with structured error output.
    """
    try:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding=encoding)
        return {"ok": True, "path": str(out), "bytes": len(content.encode(encoding))}
    except OSError as e:
        return {"ok": False, "path": path, "error": str(e)}


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python save_file.py <path> <content>")
        sys.exit(1)
    result = save_file(sys.argv[2], sys.argv[1])
    print(result)
    sys.exit(0 if result["ok"] else 1)
