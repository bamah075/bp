#!/usr/bin/env python3
"""
Malware & Security Scanner for GitHub Repositories
Checks for malicious patterns, suspicious dependencies, and security risks
"""

import os
import json
import re
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple

class SecurityScanner:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.findings = {
            "critical": [],
            "high": [],
            "medium": [],
            "low": [],
            "info": []
        }
        self.suspicious_patterns = {
            "command_injection": [
                r"os\.system\(",
                r"subprocess\..*shell=True",
                r"eval\(",
                r"exec\(",
                r"\$\(.*\)",
                r"`.*`"
            ],
            "credential_exposure": [
                r"password\s*=\s*['\"]",
                r"api[_-]?key\s*=\s*['\"]",
                r"secret\s*=\s*['\"]",
                r"token\s*=\s*['\"]",
                r"aws_access_key",
                r"private[_-]?key"
            ],
            "malicious_imports": [
                r"import\s+socket",
                r"import\s+paramiko",
                r"from\s+urllib.*import.*urlopen",
                r"requests\.get\(",
            ],
            "reverse_shell": [
                r"nc\s+-l",
                r"bash\s+-i",
                r"socket\.socket",
                r"subprocess\.(call|Popen).*bash"
            ],
            "data_exfiltration": [
                r"requests\.post.*http",
                r"urllib.*urlopen",
                r"socket\.sendall",
                r"open\(.*wb.*\).*http"
            ],
            "file_operations": [
                r"__import__\(",
                r"open\(.*[rwab]+['\"].*\)",
                r"os\.remove",
                r"shutil\.rmtree"
            ]
        }

    def scan_python_files(self) -> None:
        """Scan Python files for suspicious patterns"""
        py_files = list(self.repo_path.rglob("*.py"))

        for py_file in py_files:
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')

                    for pattern_type, patterns in self.suspicious_patterns.items():
                        for pattern in patterns:
                            for line_num, line in enumerate(lines, 1):
                                if re.search(pattern, line, re.IGNORECASE):
                                    # Filter out common false positives
                                    if not self._is_false_positive(line, pattern_type):
                                        self.findings["medium"].append({
                                            "file": str(py_file),
                                            "line": line_num,
                                            "pattern": pattern_type,
                                            "code": line.strip()[:100]
                                        })
            except Exception as e:
                self.findings["info"].append(f"Could not scan {py_file}: {str(e)}")

    def check_dependencies(self) -> None:
        """Check for known vulnerable dependencies"""
        # Check requirements.txt
        req_file = self.repo_path / "requirements.txt"
        if req_file.exists():
            with open(req_file, 'r') as f:
                deps = f.readlines()
                for dep in deps:
                    dep = dep.strip()
                    if not dep or dep.startswith('#'):
                        continue
                    self._check_vulnerable_package(dep)

        # Check setup.py
        setup_file = self.repo_path / "setup.py"
        if setup_file.exists():
            with open(setup_file, 'r') as f:
                content = f.read()
                packages = re.findall(r'install_requires\s*=\s*\[(.*?)\]', content, re.DOTALL)
                for pkg_list in packages:
                    for pkg in re.findall(r'["\']([^"\']+)["\']', pkg_list):
                        self._check_vulnerable_package(pkg)

    def _check_vulnerable_package(self, package: str) -> None:
        """Check if package is known to be vulnerable"""
        known_malicious = {
            "left-pad": "Malicious package - takes dependencies hostage",
            "npm-inject": "Malicious package",
            "browserify": "Check version, some versions had vulnerabilities",
            "colors": "Known compromised package in some versions",
        }

        pkg_name = package.split('==')[0].split('>=')[0].strip()

        if pkg_name.lower() in known_malicious:
            self.findings["critical"].append({
                "type": "known_malicious_package",
                "package": pkg_name,
                "reason": known_malicious[pkg_name.lower()]
            })

    def scan_shell_scripts(self) -> None:
        """Scan shell scripts for malicious patterns"""
        shell_files = list(self.repo_path.rglob("*.sh")) + list(self.repo_path.rglob("*.bash"))

        shell_patterns = {
            "reverse_shell": [r"bash -i >", r"nc -l", r"/dev/tcp"],
            "data_exfil": [r"curl.*|", r"wget.*|", r">.*http"],
            "privilege_escalation": [r"sudo", r"chmod 777"]
        }

        for script in shell_files:
            with open(script, 'r', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    for pattern_type, patterns in shell_patterns.items():
                        for pattern in patterns:
                            if re.search(pattern, line):
                                self.findings["high"].append({
                                    "file": str(script),
                                    "line": line_num,
                                    "type": pattern_type,
                                    "code": line.strip()[:100]
                                })

    def check_suspicious_filenames(self) -> None:
        """Check for suspicious file names and paths"""
        suspicious_names = {
            r"\.exe$": "Executable files",
            r"\.dll$": "DLL files",
            r"\.so$": "Shared object files",
            r"malware": "Malware-related names",
            r"backdoor": "Backdoor-related names",
            r"exploit": "Exploit-related names",
            r"rootkit": "Rootkit-related names",
        }

        for path in self.repo_path.rglob("*"):
            if path.is_file():
                filename = path.name.lower()
                for pattern, reason in suspicious_names.items():
                    if re.search(pattern, filename):
                        self.findings["medium"].append({
                            "type": "suspicious_filename",
                            "file": str(path),
                            "reason": reason
                        })

    def _is_false_positive(self, line: str, pattern_type: str) -> bool:
        """Filter out common false positives"""
        false_positive_indicators = [
            "# example",
            "# test",
            "docstring",
            "\"\"\"",
            "import logging",
            "log.",
            "comment",
            "TODO",
            "FIXME"
        ]

        line_lower = line.lower()
        return any(indicator in line_lower for indicator in false_positive_indicators)

    def generate_report(self) -> None:
        """Generate and display security report"""
        print("\n" + "="*70)
        print("🔒 SECURITY SCAN REPORT")
        print("="*70)
        print(f"Repository: {self.repo_path}\n")

        severity_colors = {
            "critical": "🔴 CRITICAL",
            "high": "🟠 HIGH",
            "medium": "🟡 MEDIUM",
            "low": "🟢 LOW",
            "info": "ℹ️  INFO"
        }

        total_findings = sum(len(v) for v in self.findings.values())
        print(f"Total Findings: {total_findings}\n")

        for severity, items in self.findings.items():
            if items:
                print(f"{severity_colors[severity]} ({len(items)} issues)")
                print("-" * 70)
                for item in items[:5]:  # Show first 5
                    if isinstance(item, dict):
                        for key, value in item.items():
                            print(f"  {key}: {value}")
                    else:
                        print(f"  {item}")
                    print()

                if len(items) > 5:
                    print(f"  ... and {len(items) - 5} more\n")

    def run_scan(self) -> bool:
        """Run full security scan"""
        print(f"🔍 Scanning repository: {self.repo_path}")
        print("Checking for: malware, suspicious patterns, vulnerable dependencies...\n")

        self.scan_python_files()
        self.check_dependencies()
        self.scan_shell_scripts()
        self.check_suspicious_filenames()

        self.generate_report()

        # Return True if no critical/high findings
        critical_count = len(self.findings["critical"]) + len(self.findings["high"])
        return critical_count == 0

    def get_summary(self) -> Dict:
        """Get summary of findings"""
        return {
            "critical": len(self.findings["critical"]),
            "high": len(self.findings["high"]),
            "medium": len(self.findings["medium"]),
            "low": len(self.findings["low"]),
            "safe_to_use": len(self.findings["critical"]) == 0 and len(self.findings["high"]) == 0
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python security_scanner.py <repo_path>")
        print("Example: python security_scanner.py /tmp/fastapi_mcp")
        sys.exit(1)

    repo_path = sys.argv[1]

    if not os.path.exists(repo_path):
        print(f"❌ Repository path not found: {repo_path}")
        sys.exit(1)

    scanner = SecurityScanner(repo_path)
    is_safe = scanner.run_scan()
    summary = scanner.get_summary()

    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Critical Issues: {summary['critical']}")
    print(f"High Issues: {summary['high']}")
    print(f"Medium Issues: {summary['medium']}")
    print(f"Low Issues: {summary['low']}")
    print(f"\n✅ Safe to use: {summary['safe_to_use']}" if summary['safe_to_use'] else f"\n⚠️  Review recommended: Issues found")

    sys.exit(0 if is_safe else 1)


if __name__ == "__main__":
    main()
