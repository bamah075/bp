"""
EXECUTE layer — single-purpose tool: validate_output
Non-negotiable #3: Validation Gates — simple, readable proofs.
"""
import re
import sys
import json


def validate_output(text: str, checks: list[dict]) -> dict:
    """
    Run a list of validation checks against text output.

    Each check is a dict with:
      {"type": "min_words", "value": 1000}
      {"type": "contains", "value": "##"}
      {"type": "not_contains", "value": "TODO"}
      {"type": "min_sections", "value": 3}    # counts '##' headings
      {"type": "max_words", "value": 500}

    Returns {"passed": bool, "failures": [...], "checks_run": int}
    """
    failures: list[str] = []

    for check in checks:
        t = check.get("type", "")
        v = check.get("value")

        if t == "min_words":
            count = len(text.split())
            if count < v:
                failures.append(f"min_words: {count} < {v}")

        elif t == "max_words":
            count = len(text.split())
            if count > v:
                failures.append(f"max_words: {count} > {v}")

        elif t == "contains":
            if str(v).lower() not in text.lower():
                failures.append(f"missing: '{v}'")

        elif t == "not_contains":
            if str(v).lower() in text.lower():
                failures.append(f"forbidden: '{v}'")

        elif t == "min_sections":
            sections = len(re.findall(r"^##", text, re.MULTILINE))
            if sections < v:
                failures.append(f"min_sections: {sections} < {v}")

    return {
        "passed": len(failures) == 0,
        "failures": failures,
        "checks_run": len(checks),
    }


if __name__ == "__main__":
    # CLI: python validate_output.py <file_path> <checks_json>
    if len(sys.argv) < 3:
        print("Usage: python validate_output.py <file> '<checks_json>'")
        sys.exit(1)

    from pathlib import Path
    text = Path(sys.argv[1]).read_text()
    checks = json.loads(sys.argv[2])
    result = validate_output(text, checks)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["passed"] else 1)
