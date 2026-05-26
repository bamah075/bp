#!/usr/bin/env python3
"""
Installation Permission Manager
Presents scan results and asks user for permission to install repositories
"""

import json
import sys
from pathlib import Path
from typing import List, Dict

class InstallationPermissionManager:
    def __init__(self, report_file: str = None):
        if report_file:
            self.report_file = Path(report_file)
        else:
            # Find the latest report
            scan_dir = Path("/tmp/claude_repo_scans")
            reports = sorted(scan_dir.glob("scan_report_*.json"), reverse=True)
            self.report_file = reports[0] if reports else None

        self.report = None
        if self.report_file and self.report_file.exists():
            with open(self.report_file, 'r') as f:
                self.report = json.load(f)

    def display_report(self) -> None:
        """Display the scan report in user-friendly format"""

        if not self.report:
            print("❌ No scan report found. Run the agent first.")
            return

        print("\n" + "=" * 80)
        print("📊 CLAUDE REPOSITORY SCAN REPORT")
        print("=" * 80)
        print(f"Scan Date: {self.report['scan_date']}\n")

        repos = self.report['repositories']

        # Categorize
        safe = [r for r in repos if r['recommendation'] == 'SAFE_TO_INSTALL']
        review = [r for r in repos if r['recommendation'] == 'REVIEW']
        caution = [r for r in repos if r['recommendation'] == 'CAUTION']
        blocked = [r for r in repos if r['recommendation'] == 'BLOCK']

        print(f"Summary: {len(safe)} Safe | {len(review)} Review | {len(caution)} Caution | {len(blocked)} Blocked\n")

        # Ask permission for safe repos
        if safe:
            print("=" * 80)
            print("✅ SAFE TO INSTALL")
            print("=" * 80)
            self._ask_permission_for_repos(safe, "safe")

        # Ask permission for review repos
        if review:
            print("\n" + "=" * 80)
            print("🔍 REQUIRES REVIEW")
            print("=" * 80)
            self._ask_permission_for_repos(review, "review")

        # Warn about caution repos
        if caution:
            print("\n" + "=" * 80)
            print("⚠️  PROCEED WITH CAUTION")
            print("=" * 80)
            self._ask_permission_for_repos(caution, "caution")

        # Block dangerous repos
        if blocked:
            print("\n" + "=" * 80)
            print("🔴 BLOCKED - NOT RECOMMENDED")
            print("=" * 80)
            for repo in blocked:
                print(f"\n  {repo['full_name']}")
                print(f"  ⭐ {repo['stars']} stars")
                print(f"  Reason: {repo['scan_notes']}")

    def _ask_permission_for_repos(self, repos: List[Dict], category: str) -> None:
        """Ask user permission to install repositories"""

        print()
        for i, repo in enumerate(repos, 1):
            print(f"\n[{i}/{len(repos)}] {repo['full_name']}")
            print(f"    ⭐ {repo['stars']} stars | Score: {repo['safety_score']}/100")
            print(f"    📝 {repo['description']}")
            print(f"    🔗 {repo['url']}")

            if repo['scan_notes']:
                print(f"    ℹ️  {repo['scan_notes']}")

            if repo['findings']['critical'] > 0 or repo['findings']['high'] > 0:
                print(f"    ⚠️  Issues: Critical({repo['findings']['critical']}) High({repo['findings']['high']})")

            while True:
                if category == "safe":
                    prompt = "    Install? (y/n/skip): "
                elif category == "review":
                    prompt = "    Review and install? (y/n/skip): "
                else:
                    prompt = "    Proceed with caution and install? (y/n/skip): "

                choice = input(prompt).lower().strip()

                if choice == 'y':
                    print(f"    ✅ Approved for installation: {repo['full_name']}")
                    self._handle_installation(repo)
                    break
                elif choice == 'n':
                    print(f"    ❌ Skipped: {repo['full_name']}")
                    break
                elif choice == 'skip':
                    print(f"    ⏭️  Skipped: {repo['full_name']}")
                    break
                else:
                    print("    Invalid choice. Please enter 'y', 'n', or 'skip'")

    def _handle_installation(self, repo: Dict) -> None:
        """Handle repository installation"""

        print(f"\n    🚀 Installing {repo['full_name']}...")
        print(f"    Repository URL: {repo['url']}")
        print(f"    Command: pip install {repo['name']}")
        print(f"    (Implementation would execute actual installation)")
        print(f"    ℹ️  To install manually:")
        print(f"       git clone {repo['url']}")
        print(f"       cd {repo['name']}")
        print(f"       pip install -e .")

    def interactive_mode(self) -> None:
        """Run in interactive mode"""

        if not self.report:
            print("❌ No scan report found. Run the agent first.")
            print("Usage: python3 claude_repo_agent.py")
            return

        self.display_report()

        print("\n" + "=" * 80)
        print("✅ PERMISSION REVIEW COMPLETED")
        print("=" * 80)
        print("\nApproved repositories are ready for installation.")
        print("View the full report: " + str(self.report_file))


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Installation Permission Manager")
    parser.add_argument("--report", help="Path to scan report JSON file")

    args = parser.parse_args()

    manager = InstallationPermissionManager(report_file=args.report)
    manager.interactive_mode()


if __name__ == "__main__":
    main()
