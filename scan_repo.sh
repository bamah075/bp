#!/bin/bash
# Repository Security Scanner Helper Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

REPO_URL="${1}"
SCAN_ONLY="${2:-false}"

if [ -z "$REPO_URL" ]; then
    echo -e "${RED}❌ Usage: ./scan_repo.sh <GITHUB_REPO_URL> [scan_only]${NC}"
    echo "Example: ./scan_repo.sh https://github.com/tadata-org/fastapi_mcp"
    echo "Example: ./scan_repo.sh https://github.com/tadata-org/fastapi_mcp scan_only"
    exit 1
fi

# Extract repo name from URL
REPO_NAME=$(basename "$REPO_URL" .git)
TEMP_DIR="/tmp/security_scan_${REPO_NAME}_$$"

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🔐 Repository Security Scanner${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}\n"

echo -e "${YELLOW}Repository URL:${NC} $REPO_URL"
echo -e "${YELLOW}Scan Directory:${NC} $TEMP_DIR\n"

# Clone repository
echo -e "${BLUE}1️⃣  Cloning repository...${NC}"
git clone --depth 1 "$REPO_URL" "$TEMP_DIR" 2>&1 | grep -E "(Cloning|Unpacking|Receiving)" || true

echo -e "${GREEN}✓ Repository cloned${NC}\n"

# Run Python security scanner
echo -e "${BLUE}2️⃣  Running malware/security analysis...${NC}\n"
python3 "$(dirname "$0")/security_scanner.py" "$TEMP_DIR"

SCAN_EXIT=$?

# Additional checks
echo -e "\n${BLUE}3️⃣  Checking GitHub repository metadata...${NC}\n"

# Extract owner and repo name from URL
if [[ $REPO_URL =~ github.com/([^/]+)/([^/]+) ]]; then
    OWNER="${BASH_REMATCH[1]}"
    REPO="${BASH_REMATCH[2]}"
    REPO="${REPO%.git}"

    echo "Repository: $OWNER/$REPO"
    echo "GitHub URL: https://github.com/$OWNER/$REPO"

    # Try to get repo info via GitHub API (basic check)
    echo -e "\nRepository Stats:"
    echo "  - Check: https://github.com/$OWNER/$REPO for:"
    echo "    • Number of stars (popularity indicator)"
    echo "    • Security vulnerabilities in 'Security' tab"
    echo "    • Recently updated code"
    echo "    • Active maintainers"
    echo "    • Issue history"
    echo "    • License type"
else
    echo "Could not parse repository URL"
fi

echo -e "\n${BLUE}═══════════════════════════════════════════════════${NC}"

# Cleanup
if [ "$SCAN_ONLY" != "scan_only" ]; then
    echo -e "\n${YELLOW}Cleaning up temporary files...${NC}"
    rm -rf "$TEMP_DIR"
    echo -e "${GREEN}✓ Temporary files cleaned${NC}\n"
else
    echo -e "\n${YELLOW}Scan directory preserved for manual review:${NC}"
    echo "$TEMP_DIR"
fi

if [ $SCAN_EXIT -eq 0 ]; then
    echo -e "${GREEN}✅ Security scan completed - No critical/high issues found${NC}"
    echo -e "${GREEN}Repository appears safe to integrate${NC}\n"
    exit 0
else
    echo -e "${YELLOW}⚠️  Security scan completed - Review findings above${NC}"
    echo -e "${YELLOW}Proceed with caution or investigate findings further${NC}\n"
    exit 1
fi
