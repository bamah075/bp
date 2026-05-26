# 🤖 Claude Repository Scanning Agent Configuration

Automated daily scanning of top GitHub repositories for Claude integration with built-in security analysis.

## Overview

This agent:
1. **Fetches** top Claude-related repositories daily
2. **Scans** each repository for security & quality issues
3. **Generates** a detailed report with safety scores
4. **Asks permission** before any installation
5. **Provides recommendations** based on scan results

## Components

### 1. `claude_repo_agent.py` - Main Scanning Agent
Performs the daily repository discovery and security analysis.

**Features:**
- Fetches curated top Claude repositories
- Calculates safety scores (0-100) based on:
  - Repository popularity (stars)
  - Topic analysis
  - Repository recency
  - Description analysis
- Generates JSON reports
- Provides categorized recommendations

**Usage:**
```bash
python3 claude_repo_agent.py --limit 10
python3 claude_repo_agent.py --limit 20 --output-dir /path/to/reports
```

### 2. `ask_install_permission.py` - Permission Handler
Interactive interface for reviewing scan results and requesting installation.

**Features:**
- Displays scan reports in user-friendly format
- Categories: Safe Install | Review Needed | Caution | Blocked
- Interactive prompts for each repository
- Installation command suggestions

**Usage:**
```bash
python3 ask_install_permission.py
python3 ask_install_permission.py --report /path/to/report.json
```

## Safety Score Calculation

### Score Factors (0-100):

**Popularity (Max +20)**
- 5000+ stars: +20
- 1000-5000 stars: +15
- 500-1000 stars: +10
- 100-500 stars: +5

**Topics (Max +20)**
- Trusted topics: +5 each (claude, mcp, anthropic)
- Suspicious topics: -20 (malware, crack, exploit)

**Recency (Max +10)**
- Updated < 7 days: +10
- Updated < 30 days: +5
- Updated > 365 days: -10

**Description Quality (Max -20)**
- Each suspicious word: -20 (malware, backdoor, crack)

### Recommendations:

| Score | Recommendation |
|-------|-----------------|
| 80+ | ✅ SAFE_TO_INSTALL |
| 60-79 | 🔍 REVIEW |
| 40-59 | ⚠️ CAUTION |
| <40 | 🔴 BLOCK |

Or if critical issues found: **BLOCK**

## Setting Up Daily Automation

### Option 1: Using Claude Code Loop Skill (Recommended)

```bash
/loop 24h python3 claude_repo_agent.py --limit 10
```

This will:
- Run the scan every 24 hours
- Keep you updated on new top repositories
- Generate daily reports automatically

### Option 2: Using Cron (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 9 AM):
0 9 * * * cd /home/user/bp && python3 claude_repo_agent.py --limit 10 && python3 ask_install_permission.py
```

### Option 3: GitHub Actions

Create `.github/workflows/daily_scan.yml`:

```yaml
name: Daily Claude Repo Scan

on:
  schedule:
    - cron: '0 9 * * *'  # 9 AM UTC daily

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Run repository scan
        run: |
          python3 claude_repo_agent.py --limit 10
      - name: Commit report
        run: |
          git add -A
          git commit -m "Daily Claude repo scan report"
          git push
```

## Workflow

### Daily Automated Flow:

```
┌─────────────────────────────────────────────────────┐
│  Agent runs daily                                   │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ Fetch top repos    │
        │ (GitHub search)    │
        └────────┬───────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ Security scan      │
        │ each repository    │
        └────────┬───────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ Generate report    │
        │ with findings      │
        └────────┬───────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ ASK USER PERMISSION│
        │ via interactive    │
        │ prompts            │
        └────────┬───────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
    ▼                         ▼
  APPROVE              SKIP/REJECT
    │                         │
    ▼                         ▼
INSTALL          Continue searching
```

## Example Report Output

```json
{
  "scan_date": "2026-05-26T15:30:45.123456",
  "total_repositories_scanned": 10,
  "repositories": [
    {
      "name": "fastapi_mcp",
      "full_name": "tadata-org/fastapi_mcp",
      "url": "https://github.com/tadata-org/fastapi_mcp",
      "stars": 11883,
      "description": "Expose FastAPI endpoints as MCP tools with Auth",
      "safety_score": 95,
      "recommendation": "SAFE_TO_INSTALL",
      "findings": {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
      }
    }
  ],
  "summary": {
    "safe_to_install": 6,
    "review_needed": 3,
    "caution": 1,
    "blocked": 0
  }
}
```

## Integration with Security Scanner

The agent can integrate with the security scanner (`security_scanner.py`) for deeper analysis:

```bash
# The agent will:
# 1. Identify promising repositories
# 2. Clone them locally
# 3. Run deep security scanning
# 4. Compare findings with safety scoring
# 5. Present results to user
```

## Report Storage

Reports are saved to: `/tmp/claude_repo_scans/`

```
/tmp/claude_repo_scans/
├── scan_report_20260526_093000.json
├── scan_report_20260526_173000.json
└── claude_repos_cache.json
```

View latest report:
```bash
cat /tmp/claude_repo_scans/scan_report_*.json | jq .
```

## Commands

```bash
# Run single scan
python3 claude_repo_agent.py

# Scan more repositories
python3 claude_repo_agent.py --limit 20

# Get permission prompts for latest report
python3 ask_install_permission.py

# Use specific report
python3 ask_install_permission.py --report /path/to/report.json

# Set up recurring daily scans (using Claude Code loop skill)
/loop 24h python3 claude_repo_agent.py --limit 10
```

## Customization

### Add Custom Repositories

Edit the `fetch_top_claude_repositories()` method in `claude_repo_agent.py`:

```python
custom_repos = [
    {
        "name": "my-project",
        "full_name": "user/my-project",
        "url": "https://github.com/user/my-project",
        "description": "My custom Claude integration",
        "stars": 100,
        "updated_at": "2026-05-26",
        "topics": ["claude", "custom"]
    }
]
```

### Modify Safety Scoring

Adjust weights in `_calculate_safety_score()` method for your preferences.

### Change Report Format

Modify `generate_report()` to output in different formats (CSV, HTML, etc.)

## Troubleshooting

### No reports generated
```bash
ls -la /tmp/claude_repo_scans/
python3 claude_repo_agent.py --output-dir /tmp/test
```

### Permission script not interactive
```bash
# Make sure Python is running in interactive mode
python3 -i ask_install_permission.py
```

### Loop not running
```bash
# Check if loop is active
/help loop
# Start new loop
/loop 24h python3 claude_repo_agent.py --limit 10
```

## Security Considerations

✅ **What This Protects Against:**
- Popularity-based reputation (star count)
- Suspicious project descriptions
- Inactive/abandoned projects
- Clearly malicious repository names

⚠️ **Limitations:**
- Shallow analysis (reputation-based, not deep code scanning)
- No real-time malware detection
- Relies on publicly available metadata
- For full security, combine with `security_scanner.py`

## Next Steps

1. **Set up daily automation** using `/loop 24h` command
2. **Configure security preferences** in the agent
3. **Review recommendations** when prompted
4. **Monitor scan reports** in `/tmp/claude_repo_scans/`
5. **Integrate with CI/CD** for automated checks

---

**Example Daily Flow:**
```
Day 1: Agent fetches 10 top repos, scans them, shows you options
Day 2: Agent fetches another batch, updates recommendations
Day 3: You approve installations from Day 1
Day 4: New batch discovered...
```

The agent keeps you informed daily while respecting your permission decisions.
