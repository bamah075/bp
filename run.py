#!/usr/bin/env python3
"""
Agent Teams — CLI entry point.
Run any of the 7 agent team patterns from the command line.

Usage:
  python run.py <team_number> [options]

Examples:
  python run.py 1 --transcript path/to/transcript.md
  python run.py 2
  python run.py 3
  python run.py 4
  python run.py 5
  python run.py 6
  python run.py 7
"""
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def main():
    parser = argparse.ArgumentParser(
        description="Run an Agent Team prompt",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Teams:
  1  Content Repurposing Pipeline   — 1 transcript → 4 platform pieces
  2  Pitch Deck Builder             — Research → Slides → .pptx (sequential)
  3  RFP Response Generator         — Parallel analysis → full proposal
  4  Competitive Intelligence       — 4 analysts → synthesis battlecard
  5  Advisory Board Decision        — 5 agents debate → GO/NO-GO brief
  6  Marketing Campaign Launch      — Email + Social + Ads + Landing Page
  7  Personal AI Business Assistant — Telegram bot with skill routing + memory
        """,
    )
    parser.add_argument("team", type=int, choices=range(1, 8), help="Team number (1-7)")
    parser.add_argument("--transcript", default="transcript.md", help="[Team 1] Path to transcript file")
    parser.add_argument("--rfp-url", default=None, help="[Team 3] Override RFP URL")
    parser.add_argument("--no-approval", action="store_true", help="[Teams 2,7] Skip plan approval gates")

    args = parser.parse_args()

    require_approval = not args.no_approval

    if args.team == 1:
        if not Path(args.transcript).exists():
            print(f"Creating sample transcript at {args.transcript}...")
            Path(args.transcript).write_text(
                "# Sample Transcript\n\nThis is a sample transcript. "
                "Replace this file with your actual video transcript content.\n\n"
                "Key point 1: AI agents are transforming how teams work...\n"
                "Key point 2: The shift from single models to multi-agent systems...\n"
                "Key point 3: Practical patterns for building agent teams today..."
            )
        from agent_teams.teams.t01_content_repurposing import run
        run(transcript_path=args.transcript)

    elif args.team == 2:
        from agent_teams.teams.t02_pitch_deck_builder import run
        run(require_approval=require_approval)

    elif args.team == 3:
        from agent_teams.teams.t03_rfp_response import run
        kwargs = {}
        if args.rfp_url:
            kwargs["rfp_url"] = args.rfp_url
        run(**kwargs)

    elif args.team == 4:
        from agent_teams.teams.t04_competitive_intel import run
        run()

    elif args.team == 5:
        from agent_teams.teams.t05_advisory_board import run
        run()

    elif args.team == 6:
        from agent_teams.teams.t06_marketing_campaign import run
        run()

    elif args.team == 7:
        from agent_teams.teams.t07_pa_assistant import run
        run(require_approval=require_approval)


if __name__ == "__main__":
    main()
