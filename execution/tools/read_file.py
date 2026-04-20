"""
EXECUTE layer — single-purpose tool: read_file
"""
import sys
from pathlib import Path


def read_file(path: str, encoding: str = "utf-8") -> dict:
    """Read file content. Returns typed result dict."""
    try:
        p = Path(path)
        if not p.exists():
            return {"ok": False, "path": path, "error": "File not found"}
        content = p.read_text(encoding=encoding)
        return {"ok": True, "path": str(p), "content": content, "bytes": p.stat().st_size}
    except OSError as e:
        return {"ok": False, "path": path, "error": str(e)}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python read_file.py <path>")
        sys.exit(1)
    result = read_file(sys.argv[1])
    if result["ok"]:
        print(result["content"])
    else:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
